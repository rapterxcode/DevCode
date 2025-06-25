import { createBrowserRouter } from 'react-router-dom'
import Home from '../pages/Home.tsx'
import Login from '../pages/Login.tsx'

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "/login",
    element: <Login />,
  },
], {
  basename: '/'
})

export default router 