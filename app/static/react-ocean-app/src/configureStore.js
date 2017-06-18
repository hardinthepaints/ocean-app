import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk';
import createLogger from 'redux-logger'
import rootReducer from './reducers'


//if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
//    // dev code
//    const loggerMiddleWare = createLogger();
//
//} else {
//    // production code
//}

export default function configureStore( preloadedState ){
    
    /* Create a logger if in dev mode, else do not have a logger*/
    const middleware = (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') ?
        applyMiddleware(thunkMiddleware,createLogger()) : applyMiddleware(thunkMiddleware)

        
    return createStore(
        rootReducer,
        preloadedState,
        middleware
    )
}