import './App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Storage from "./pages/Storage";
import Login from "./pages/Login";
import Register from "./pages/Register";
import ErrorPage from "./pages/ErrorPage";

function App() {
    return (
        <div className="App">
            <div className={"navigation"}>
                <nav>
                    <ul>
                        <li>
                            <a href={"/login"}>Login</a>
                            <a href={"/register"}>Register</a>
                            <a href={"/storage"}>Storage</a>
                        </li>
                    </ul>
                </nav>
            </div>

            <BrowserRouter>
                <Routes>
                    <Route path={"/storage"} element={<Storage/>}/>
                    <Route path={"/login"} element={<Login/>}/>
                    <Route path={"/register"} element={<Register/>}/>
                    <Route path={"/error"} element={<ErrorPage/>}/>
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
