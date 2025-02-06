async function get_all_roles_permissions(role_profile) {
    let roles = await frappe.call({
        method: 'sva_frappe.apis.user_permissions.get_roles_and_permissions_by_profile',
        args: {
            role_profile: role_profile
        },
    });
    return roles.message;
}

const role_and_permission_popup = async (frm) => {
    try {
        const roles = await get_all_roles_permissions(frm.doc.role_profile);
        // console.log(roles,'roles');
        if (!roles || roles.message) {
            frm.fields_dict.module_permissions.$wrapper.html(`
                <div class="p-4 text-center text-muted">
                    ${roles?.message || 'No permissions found'}
                </div>
            `);
            return;
        }

        // Define all possible permissions
        const permissions = [
            "read",
            "write",
            "create",
            "delete",
            "submit",
            "cancel",
            "amend",
            "email",
            "export",
            "import",
            "print",
            "report",
            "select",
            "share"
        ];

        // Group permissions by document type
        const groupedPermissions = {};
        roles.roles_and_permissions.forEach(item => {
            const doctype = item.parent;
            if (!groupedPermissions[doctype]) {
                groupedPermissions[doctype] = {
                    doctype: doctype,
                    levels: {}
                };
            }
            
            const level = item.permissions.permlevel;
            if (!groupedPermissions[doctype].levels[level]) {
                groupedPermissions[doctype].levels[level] = {
                    roles: [],
                    permissions: {}
                };
            }
            
            groupedPermissions[doctype].levels[level].roles.push(item.role);
            permissions.forEach(perm => {
                const permKey = perm.toLowerCase();
                if (item.permissions[permKey]) {
                    groupedPermissions[doctype].levels[level].permissions[permKey] = true;
                }
            });
        });

        // Create table header
        const headerRow = `
            <tr>
                <th class="text-left" style="min-width: 200px;">Document Type</th>
                <th>Level</th>
                <th class="text-left">Roles</th>
                ${permissions.map(perm => `<th>${perm}</th>`).join('')}
            </tr>
        `;

        // Create table rows
        const tableRows = Object.values(groupedPermissions).map(docPerms => {
            return Object.entries(docPerms.levels).map(([level, levelData]) => {
                return `
                    <tr>
                        <td class="text-left">${docPerms.doctype}</td>
                        <td>${level}</td>
                        <td class="text-left">
                            <div class="roles-cell">
                                ${levelData.roles.join(', ')}
                            </div>
                        </td>
                        ${permissions.map(perm => {
                            const permValue = levelData.permissions[perm.toLowerCase()] || false;
                            return `<td>${permValue ? '✓' : '-'}</td>`;
                        }).join('')}
                    </tr>
                `;
            }).join('');
        }).join('');

        // Render the complete table
        frm.fields_dict.module_permissions.$wrapper.html(`
            <div class="permission-table-container">
                <style>
                    .permission-table-container {
                        padding: 15px;
                        overflow-x: auto;
                    }
                    .permission-table {
                        width: 100%;
                        border-collapse: collapse;
                        font-size: 13px;
                    }
                    .permission-table th,
                    .permission-table td {
                        padding: 8px;
                        text-align: center;
                        border-bottom: 1px solid #d1d5db;
                    }
                    .permission-table th {
                        background-color: #f3f4f6;
                        font-weight: 500;
                        white-space: nowrap;
                    }
                    .permission-table td {
                        color: #4b5563;
                    }
                    .text-left {
                        text-align: left !important;
                    }
                    .permission-table tr:hover {
                        background-color: #f9fafb;
                    }
                    .roles-cell {
                        max-width: 200px;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    }
                </style>
                <table class="permission-table">
                    <thead>
                        ${headerRow}
                    </thead>
                    <tbody>
                        ${tableRows}
                    </tbody>
                </table>
            </div>
        `);
    } catch (error) {
        console.error('Error loading permissions:', error);
        frm.fields_dict.module_permissions.$wrapper.html(`
            <div class="p-4 text-center text-muted">
                Error loading permissions. Please try again.
            </div>
        `);
    }
};