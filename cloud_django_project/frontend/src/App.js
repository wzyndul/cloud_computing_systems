import './App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Storage from "./pages/Storage";
import ErrorPage from "./pages/ErrorPage";

function App() {
    return (
        <div className="App">
            <nav>
                <ul>
                    <li>
                        <a href={"/"}>Home</a>
                        <a href={"/storage"}>Storage</a>
                    </li>
                </ul>
            </nav>

            <header className="App-header">
                <BrowserRouter>
                    <Routes>
                        <Route path={"/storage"} element={<Storage/>}/>
                        <Route path={"/error"} element={<ErrorPage/>}/>
                    </Routes>
                </BrowserRouter>
            </header>
        </div>
    );
}

export default App;
