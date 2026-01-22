class Selectors:
    # Login Page
    USERNAME_INPUT = "input[name='field-username'], input[autocomplete='username']"
    PASSWORD_INPUT = "input[name='field-password'], input[autocomplete='current-password']"
    LOGIN_BUTTON = "button[type='submit'], button:has-text('Entrar'), button:has-text('Login')"

    # Dashboard / Program Selection (Accordion Style)
    PROGRAM_PANEL = ".v-expansion-panel"
    PROGRAM_HEADER = ".v-expansion-panel-header"
    PROGRAM_TITLE = ".my-programs-panels__header--block"
    
    # Generic Close Modal
    CLOSE_MODAL_BUTTON = "#action-close-first-access, div.v-dialog--active button:has(i.mdi-close), button[aria-label='Close'], button[aria-label='Fechar'], .modal-close, button:has-text('Fechar'), [data-dismiss='modal']"
    
    # Inside Program (Volume Tabs)
    VOLUME_TAB = ".secad-custom-tabs__header--tab button"
    VOLUME_TAB_ACTIVE = ".secad-custom-tabs__header--tab.active button"
    
    # Article List
    ARTICLE_LINK = ".secad-custom-tabs__content a.item"

    # Article Page Navigation
    NEXT_BUTTON = "a.next_prev_btn:has(i.mdi-chevron-right), .article_title + a:has(i.mdi-chevron-right)"
    PREV_BUTTON = "a.next_prev_btn:has(i.mdi-chevron-left), button:has-text('Anterior'), [aria-label='Anterior']"
    MARK_READ_BUTTON = "div.check_container, button.circle-container-checked"
    
    # Interactive Elements inside Article
    IMAGE_ZOOMABLE = "img.zoomable, img[data-zoom], figure img" 
    
    # Questions / Quiz
    QUESTION_CONTAINER = "div[id^='opc']" # Container often has id like opc1R
    ALTERNATIVE_OPTION = "button._b-Atividade-alternativa"
    CHECK_ANSWER_BUTTON = "button._r-Atividade-Resposta"
