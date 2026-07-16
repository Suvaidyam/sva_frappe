LEVEL_FIELDS = ["state", "district", "block", "gram_panchayat", "village"]


def _row_path(row):
	"""Return the populated ancestor tuple for a row, trimmed at the first empty field."""
	path = []
	for field in LEVEL_FIELDS:
		value = row.get(field) if isinstance(row, dict) else row.get(field)
		if not value:
			break
		path.append(value)
	return tuple(path)


def merge_level_selection(existing_rows, level, scope, selected):
	"""
	Level-scoped, cascade-aware merge for a single wizard step's Save.

	- level: one of LEVEL_FIELDS ("state"/"district"/"block"/"gram_panchayat"/"village") - the
	  level being saved.
	- scope: list of ancestor-tuples defining which parents are currently in view for this save
	  (e.g. for level="district", the currently-selected state-id tuples). Ignored for
	  level == "state", which has no parent and is always universally in scope.
	- selected: list of fully-qualified tuples (through `level`) for whatever is currently
	  checked at that level, within scope.

	Rows whose ancestor prefix isn't in `scope` are out of scope for this save and are left
	completely untouched - e.g. saving Bihar's districts never reads or affects Delhi's rows.
	Within scope: a path present in both existing and selected is kept exactly as-is (preserving
	whatever deeper data already exists under it); a path only in existing is deleted along with
	everything beneath it (cascade delete - the user unchecked it and saved here); a path only in
	selected is inserted as a new row. A bare parent-only row (e.g. a state with no district
	chosen yet) is superseded once `selected` gains any path under it.
	"""
	level_index = LEVEL_FIELDS.index(level)
	scope_tuples = {tuple(s) for s in (scope or [])}
	selected_tuples = {tuple(s) for s in (selected or [])}

	def in_scope(path):
		if level_index == 0:
			return True
		return path[:level_index] in scope_tuples

	existing_paths = set()
	rows_by_path = {}
	pass_through_rows = []

	for row in existing_rows:
		path = _row_path(row)
		if not path:
			continue

		if not in_scope(path):
			pass_through_rows.append(row)
			continue

		if len(path) > level_index:
			level_path = path[: level_index + 1]
			existing_paths.add(level_path)
			rows_by_path.setdefault(level_path, []).append(row)
		else:
			# bare row shallower than this level - superseded once `selected` gains a path
			# under it, otherwise kept as-is (parent still selected, nothing chosen here yet)
			has_selected_child = any(s[: len(path)] == path for s in selected_tuples)
			if not has_selected_child:
				pass_through_rows.append(row)

	merged_rows = list(pass_through_rows)

	for level_path, rows in rows_by_path.items():
		if level_path in selected_tuples:
			merged_rows.extend(rows)

	for level_path in selected_tuples:
		if level_path in existing_paths or not in_scope(level_path):
			continue
		row = {field: None for field in LEVEL_FIELDS}
		for i, value in enumerate(level_path):
			row[LEVEL_FIELDS[i]] = value
		merged_rows.append(row)

	return merged_rows


def merge_full_path(existing_rows, level_selections):
	"""
	Apply merge_level_selection once per level, in order (State first, then District, etc, up
	through whichever level the wizard's current step reaches). Running them in sequence - each
	level's output feeding the next level's input - is what makes cascading work correctly: if a
	state gets unchecked, the State-level pass removes it (and everything beneath it) before the
	District-level pass even runs, so a save triggered from a deeper step still correctly applies
	an ancestor-level uncheck instead of leaving it stranded until the user happens to click Save
	on that ancestor's own step.
	"""
	rows = existing_rows
	for entry in level_selections or []:
		rows = merge_level_selection(rows, entry["level"], entry.get("scope"), entry.get("selected"))
	return rows
