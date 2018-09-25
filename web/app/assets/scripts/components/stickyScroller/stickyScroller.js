// v 1.1.3
// TODO: position:absolute/static adaptive
// TODO: refactor Math.max/min with readable code
class StickyScroller {

    element = null;
    reference = null;
    breakpointFrom = null;
    breakpointTo = null;
    onlyTop = false;
    onlyBottom = false;
    lastScroll = 0;
    elementTranslate = 0;
    offsetTop = 0;
    offsetBottom = 0;
    fresh = true;

    constructor(options) {
        this.element = options.object;
        this.reference = options.reference;
        this.breakpointFrom = options.breakpointFrom || null;
        this.breakpointTo = options.breakpointTo|| null;
        this.onlyTop = options.onlyTop || false;
        this.onlyBottom = options.onlyBottom|| false;
        this.offsetTop = options.offsetTop || 0;
        this.offsetBottom = options.offsetBottom || 0;

        window.addEventListener('resize', this.checkScreen);
        this.checkScreen();
    }
    checkScreen = () => {
        let windowWidth = window.innerWidth;
        if (this.breakpointFrom !== null ? windowWidth >= this.breakpointFrom : true && this.breakpointTo !== null ? windowWidth <= this.breakpointTo : true) {
            this.activateScroller();
        } else {
            this.deactivateScroller();
        }
    }
    activateScroller = () => {
        window.addEventListener('scroll', this.scrollController);
        this.scrollController();
    }
    deactivateScroller = () => {
        window.removeEventListener('scroll', this.scrollController);
        this.resetValue(0);
    }
    scrollController = () => {
        if (window.getComputedStyle(document.body, null).getPropertyValue("position") !== 'fixed') {
            let windowScroll = window.pageYOffset;
            let windowHeight = window.innerHeight;
            let elementHeight = this.element.offsetHeight;
            let elementTop = this.element.offsetTop;
            let referenceHeight = this.reference.offsetHeight - this.offsetTop - this.offsetBottom;
            let referenceTop = this.reference.offsetTop + this.offsetTop;
            let delta = windowScroll - this.lastScroll;
            this.lastScroll = windowScroll;
            let scrollDownHandler = () => {
                this.elementTranslate = Math.min(Math.max(this.elementTranslate - delta, bottomLimit), Math.min(this.elementTranslate, topLimit));
            }
            let scrollUpHandler = () => {
                this.elementTranslate = Math.min(Math.min(Math.max(this.elementTranslate - delta, bottomLimit), topLimit), Math.max(this.elementTranslate, topLimit));
            }
    
            let topLimit = Math.max(referenceTop - windowScroll - elementTop, 0);
            let bottomLimit = Math.min(referenceTop + referenceHeight - windowScroll - elementHeight - elementTop, windowHeight - elementHeight);
            if (referenceHeight < elementHeight) {
                this.reference.style.minHeight = elementHeight + 'px';
            }
    
            if (this.fresh) {
                this.elementTranslate = referenceTop + referenceHeight < windowScroll + elementHeight ? bottomLimit : topLimit;
                this.fresh = false;
            } else {
                if (delta >= 0) { // scrolling down
                    if (!this.onlyTop) {
                        scrollDownHandler();
                    }
                } else { // scrolling up
                    if (!this.onlyBottom) {
                        scrollUpHandler();
                    }
                }
            }
            this.setValue(this.elementTranslate);
        }
    }
    setValue = (value) => {
        let translateValue = 'translateY(' + value + 'px)';
        this.element.style.transform = translateValue;
        this.element.style.webkitTransform = translateValue;
        this.element.style.mozTransform = translateValue;
        this.element.style.msTransform = translateValue;
        this.element.style.oTransform = translateValue;
    }
    resetValue = () => {
        this.element.style.removeProperty('transform');
        this.element.style.removeProperty('webkitTransform');
        this.element.style.removeProperty('mozTransform');
        this.element.style.removeProperty('msTransform');
        this.element.style.removeProperty('oTransform');
    }
}

export default StickyScroller;