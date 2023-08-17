import { createApp, provide, h } from 'vue'
import App from './App.vue'
import router from './router'

import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'
import { DefaultApolloClient } from '@vue/apollo-composable'

// apollo config
const httpLink = createHttpLink({
    //uri: 'https://spacex-production.up.railway.app/',
    uri: 'http://localhost:8000/graphql',
})

const cache = new InMemoryCache()

const apolloClient = new ApolloClient({
    link: httpLink,
    cache,
})

const app = createApp({
    setup() {
        provide(DefaultApolloClient, apolloClient)
    },

    render: () => h(App),
})

app.use(router)

app.mount('#app')
