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
    console.log(theme, "theme");
    const style = document.createElement('style');
    style.innerHTML = `
        


            #page-login {
                background: ${theme.page_background_type && theme.page_background_type == 'Color' ? `${theme.login_page_background_color}` : theme.page_background_type == 'Image' ? theme.login_page_background_image && `url("${theme.login_page_background_image}")` : 'transparent'} !important;
                background-size: cover !important;
                height: 100vh !important;
                z-index: 1000;
                /* background-color: transparent !important; */
            }
            .btn-primary.btn-login {
                background-color: ${theme.login_button_background_color && theme.login_button_background_color} !important;
                color: ${theme.login_button_text_color && theme.login_button_text_color} !important;
            }
            .btn-primary.btn-login:hover {
                background-color: ${theme.login_page_button_hover_background_color && theme.login_page_button_hover_background_color} !important;
                color: ${theme.login_page_button_hover_text_color && theme.login_page_button_hover_text_color} !important;
            }
            .for-login {
                position: ${theme.login_box_position !== 'Default' ? 'absolute' : ''};
                right: ${theme.login_box_position === 'Right' ? '15%' : ''};
                left: ${theme.login_box_position === 'Left' ? '15%' : ''};
            }
            .login-content.page-card{
                padding: ${theme.login_box_position !== 'Default' ? '50' : ''}px;
                background-color: ${theme.login_box_background_color && theme.login_box_background_color} !important;
                border: 2px solid ${theme.login_box_background_color && theme.login_box_background_color} !important;
            }
            .page-card-head h4 {
                color: ${theme.page_heading_text_color && theme.page_heading_text_color} !important;
            }
        
            @media (max-width: 768px) {
                .for-login {
                    position: static;
                    right: 0%;
                    left: 0%;
                }
                .login-content.page-card{
                    padding: auto auto;
                }
            }

          

            .navbar {
                background-color: ${theme.navbar_color && theme.navbar_color} !important;
            }
            .navbar.container {
                color: ${theme.navbar_text_color && theme.navbar_text_color} !important;
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

    

        .btn-primary {
            background-color: ${theme.button_background_color && theme.button_background_color} !important;
        }
        .btn-primary span{
            color: ${theme.button_text_color && theme.button_text_color} !important;
        }
        .btn-primary svg.icon.icon-xs use{
            stroke: ${theme.button_text_color && theme.button_text_color} !important;
        }
        .d-lg-block,
        .d-sm-block {
            display: none !important;
        }
        


        .content.page-container{
            background-color: ${theme.body_background_color && theme.body_background_color} !important;
        }
        .page-head {
            background-color: ${theme.body_background_color && theme.body_background_color} !important;
        }
        .layout-main-section{
            background-color: ${theme.main_body_content_box_background_color && theme.main_body_content_box_background_color} !important;
        }
    `;

    document.head.appendChild(style);
}
applyTheme()