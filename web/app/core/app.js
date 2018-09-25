class App {
    components = [];

    _getComponentName = (Component) => {
        return Component.name || Component.toString().match(/^function\s*([^\s(]+)/)[1];
    }

    setComponents(components) {
        components.forEach(Component => {
            this.components.push({
                Component,
                name: this._getComponentName(Component),
                instances: []
            });
        });
    }

    getComponentByName = (name) => {
        return this.components.filter(x => x.name === name)[0];
    }
    getComponentClassByName = (name) => {
        const component = this.getComponentByName(name);
        return component !== null ? component.Component : null;
    }
    getComponentInstancesByName = (name) => {
        const component = this.getComponentByName(name);
        return component !== null ? component.instances : null;
    }
    getInstancesByNode = (node, name = null) => {
        if (name !== null) {
            const component = this.getComponentByName(name);
            const instances = component !== null ? component.instances.filter(x => x.node === node) : [];
            return instances.map(x => x.instance);
        }

        const components = [];
        this.components.forEach(component => {
            const instances = component.instances.filter(x => x.node === node);
            if (instances.length > 0) {
                components.push({
                    componentName: component.name,
                    instances: instances.map(x => x.instance)
                });
            }
        });
        return components;
    }
    
    initializeComponents() {
        this.components.forEach(component => {
            if (component.Component.selector === undefined || component.Component.selector === null) {
                return;
            }
            const nodeList = document.querySelectorAll(component.Component.selector);
            
            for (let i = 0; i < nodeList.length; i++) {
                const node = nodeList[i];
                if (node.dataset.appComponentInitalized) {
                    continue;
                }
                node.dataset.appComponentInitalized = true;
                component.instances.push({
                    node,
                    instance: new component.Component(node)
                });
            }
        });
    }
}

const app = new App();
window.app = app;

export default app;