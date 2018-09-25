import App from '../core/app';

// Layouts
import LayoutGlobal from './scripts/layouts/global';
import LayoutDashboard from './scripts/layouts/dashboard';

// Pages
import PageAuth from './scripts/pages/auth';

// Components
import ComponentForm from './scripts/components/form/form';
import ComponentBuy from './scripts/components/buy/buy';
import ComponentInvest from './scripts/components/invest/invest';
import ComponentToggler from './scripts/components/toggler/toggler';
import ComponentModal from './scripts/components/modal/modal';

App.setComponents([
  LayoutGlobal,
  LayoutDashboard,

  PageAuth,

  ComponentForm,
  ComponentBuy,
  ComponentInvest,
  ComponentToggler,
  ComponentModal,
]);

document.addEventListener('DOMContentLoaded', () => {
  App.initializeComponents();
});