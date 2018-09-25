
class LayoutDashboard {
    static selector = '[data-layout-dashboard]';

    selectors = {
        sidebar: '[data-layout-dashboard-child="sidebar"]',
        sidebarOpen: '[data-layout-dashboard-child="sidebarOpen"]',
        sidebarClose: '[data-layout-dashboard-child="sidebarClose"]',
    };
    children = {
        sidebar: null,
        sidebarOpen: null,
        sidebarCloseAll: null,
    };
    options = {
        sidebarActiveClass: 'layout-dashboard__sidebar_active',
    };
    root = null;

    constructor(element) {
        this.root = element;

        this.initChildren();
        this.initSidebarOpen();
        this.initSidebarCloseAll();
    }

    initChildren = () => {
        this.children.sidebar = this.root.querySelector(this.selectors.sidebar);
        this.children.sidebarOpen = this.root.querySelector(this.selectors.sidebarOpen);
        this.children.sidebarCloseAll = this.root.querySelectorAll(this.selectors.sidebarClose);
    }

    initSidebarOpen = () => {
        this.children.sidebarOpen.addEventListener('click', this.sidebarOpen);
    }
    initSidebarCloseAll = () => {
        for (let i = 0; i < this.children.sidebarCloseAll.length; i++) {
            const item = this.children.sidebarCloseAll[i];
            item.addEventListener('click', this.sidebarClose);
        }
    }
    sidebarOpen = () => {
        this.children.sidebar.classList.add(this.options.sidebarActiveClass);
    }
    sidebarClose = () => {
        this.children.sidebar.classList.remove(this.options.sidebarActiveClass);
    }
}

export default LayoutDashboard;