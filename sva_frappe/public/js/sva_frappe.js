const getTheme = async () => {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: "sva_frappe.api.get_my_theme",
            freeze: true,
            callback: async function (response) {
                resolve(response?.message || response)
            }
        });
    })
}
const applyTheme = async () => {
    let theme = await getTheme()
    const style = document.createElement('style');
    style.innerHTML = `
        .btn-primary {
            background-color: ${theme.button_background_color && theme.button_background_color} !important;
        }
        .btn-primary span , .btn-primary.btn-login{
            color: ${theme.button_text_color && theme.button_text_color} !important;
        }
        .btn-primary svg.icon.icon-xs use{
            stroke: ${theme.button_text_color && theme.button_text_color} !important;
        }

        .navbar {
            background-color: ${theme.navbar_color && theme.navbar_color} !important;
        }

        #navbar-breadcrumbs li a {
            color: ${theme.navbar_text_color && theme.navbar_text_color} !important;
        }

        .navbar li a::before {
            stroke:${theme.navbar_icon_color && theme.navbar_icon_color};
        }

        .navbar svg.es-icon.icon-sm use {
            stroke:${theme.navbar_icon_color && theme.navbar_icon_color};
        }

        .d-lg-block,
        .d-sm-block {
            display: none !important;
        }

        #page-login {
            background-image: url("https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0");
            background-size: cover !important;
            height: 100vh !important;
            z-index: 1000;
            /* background-color: transparent !important; */
        }

        .for-login {
            margin-left: 650px;
        }

        /* Media queries for responsiveness */
        @media (max-width: 1200px) {
            .for-login {
                margin-left: 500px;
            }
        }

        @media (max-width: 992px) {
            .for-login {
                margin-left: 300px;
            }
        }

        @media (max-width: 768px) {
            .for-login {
                margin-left: 20px;
            }
        }

        @media (max-width: 576px) {
            .for-login {
                margin-left: 10px;
                width: calc(100% - 20px);
            }
        }
    `;
    document.head.appendChild(style);
}
applyTheme()