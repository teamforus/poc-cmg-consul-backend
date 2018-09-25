class FormDropdown {
    static selector = '[data-form-dropdown]';
    static openedSelect = null;

    selectors = {
        select: 'select',
    };
    children = {
        select: null,
        selected: null,
        optionsWrapper: null,
        options: null,
    };
    options = {
        dropdownActiveClass: 'ui-form__dropdown_active',
        dropdownSelectedClass: 'ui-form__dropdown-selected',
        dropdownSelectedDisabledClass: 'ui-form__dropdown-selected_disabled',
        dropdownOptionsWrapperClass: 'ui-form__dropdown-options',
        dropdownOptionClass: 'ui-form__dropdown-options-item',
        dropdownOptionActiveClass: 'ui-form__dropdown-options-item_active',
        dropdownOptionDisabledClass: 'ui-form__dropdown-options-item_disabled',
    };
    root = null;
    opened = false;
    activeOptionIndex = 0;

    constructor(element) {
        this.root = element;

        this.initChildren();
        this.initDropdown();
    }
    initChildren = () => {
        this.children.select = this.root.getElementsByTagName(this.selectors.select)[0];
    }
    createSelected = () => {
        const selected = document.createElement("div");
        selected.setAttribute("class", this.options.dropdownSelectedClass);
        selected.innerHTML = this.children.select.options[this.children.select.selectedIndex].innerHTML;
        if (this.children.select.options[this.children.select.selectedIndex].disabled) {
            selected.classList.add(this.options.dropdownSelectedDisabledClass);
        }
        this.root.appendChild(selected);
        this.children.selected = selected;
    }
    createOptionsWrapper = () => {
        const optionsWrapper = document.createElement("div");
        optionsWrapper.setAttribute("class", this.options.dropdownOptionsWrapperClass);
        this.root.appendChild(optionsWrapper);
        this.children.optionsWrapper = optionsWrapper;
    }
    createOptions = () => {
        this.activeOptionIndex = this.children.select.selectedIndex;

        for (let i = 0; i < this.children.select.length; i++) {
            /*for each option in the original select element,
            create a new DIV that will act as an option item:*/
            let optionCopy = document.createElement("div");
            optionCopy.setAttribute("class", this.options.dropdownOptionClass);

            if (this.activeOptionIndex === i) {
                optionCopy.classList.add(this.options.dropdownOptionActiveClass);
            }
            if (this.children.select.options[i].disabled) {
                optionCopy.classList.add(this.options.dropdownOptionDisabledClass);
            }
            optionCopy.innerHTML = this.children.select.options[i].innerHTML;
            optionCopy.addEventListener("click", () => {
                this.selectOption(i)
            });
            this.children.optionsWrapper.appendChild(optionCopy);
        }
        this.children.options = this.children.optionsWrapper.children;
    }
    selectOption = (index) => {
        this.children.options[this.activeOptionIndex].classList.remove(this.options.dropdownOptionActiveClass);
        this.children.select.options[this.activeOptionIndex].selected = false;
        this.children.options[index].classList.add(this.options.dropdownOptionActiveClass);
        this.children.select.options[index].selected = true;
        this.children.select.selectedIndex = index;

        this.activeOptionIndex = index;
        this.children.selected.innerHTML = this.children.options[index].innerHTML;
        if (this.children.selected.classList.contains(this.options.dropdownSelectedDisabledClass)) {
            this.children.selected.classList.remove(this.options.dropdownSelectedDisabledClass);
        }
    }
    initDropdown = () => {
        this.createSelected();
        this.createOptionsWrapper();
        this.createOptions();
        document.addEventListener("click", () => {
            if (this.root.classList.contains(this.options.dropdownActiveClass)) {
                this.root.classList.remove(this.options.dropdownActiveClass);
                FormDropdown.openedSelect = null;
            }
        });
        this.children.selected.addEventListener("click", (e) => {
            e.stopPropagation();
            if (this.root.classList.contains(this.options.dropdownActiveClass)) {
                this.root.classList.remove(this.options.dropdownActiveClass);
            } else {
                this.root.classList.add(this.options.dropdownActiveClass);
                if (FormDropdown.openedSelect !== null && FormDropdown.openedSelect !== this.root) {
                    FormDropdown.openedSelect.classList.remove(this.options.dropdownActiveClass);
                }
                FormDropdown.openedSelect = this.root;
            }
            //this.root.classList.toggle(this.options.dropdownActiveClass);
            //console.log(this.children.optionsWrapper.getBoundingClientRect().bottom, document.body.clientHeight);
        });
    }
}

export default FormDropdown;