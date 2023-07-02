import Vue from 'vue'
import App from './App.vue'
import router from './router'
import Amplify, * as AmplifyModules from 'aws-amplify'
import { AmplifyPlugin } from 'aws-amplify-vue'
import { BootstrapVue } from 'bootstrap-vue'

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(AmplifyPlugin, AmplifyModules)
Vue.use(BootstrapVue)

Vue.config.productionTip = false

const data = require("../../../cdk-outputs.json")
const userPoolId = data["CognitoProjectStack"]["userPoolId"]
const userPoolWebClientId = data["CognitoProjectStack"]["userPoolWebClientId"]
const authDomain = data["CognitoProjectStack"]["AuthDomain"]
const signIn = data["CognitoProjectStack"]["RedirectSignIn"]
const signOut = data["CognitoProjectStack"]["RedirectSignOut"]

Amplify.configure({
  Auth: {
    region: 'us-east-1',
    userPoolId: userPoolId,
    userPoolWebClientId: userPoolWebClientId,
    oauth: {
      domain: authDomain,
      scope: ['email', 'profile', 'openid'],
      redirectSignIn: signIn,
      redirectSignOut: signOut,
      responseType: 'code'
    }
  }
});

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
