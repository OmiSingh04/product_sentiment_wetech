import Home from "./pages/Home"
import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Link } from "react-router-dom"
import Products from "./pages/Products"
import Product from "./pages/Product"


function App() {

return (
    <BrowserRouter>
<nav style={{
        display: "flex",
        alignItems: "center",
        padding: "12px 24px",
        backgroundColor: "#007BFF",
        color: "white",
        boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
        position: "sticky",
        top: 0,
        marginBottom: "12px",
        zIndex: 1000
      }}>
        <Link to="/" style={{ display: "flex", alignItems: "center", gap: "10px", textDecoration: "none", color: "white" }}>
          <span style={{ fontSize: "24px" }}>🛒</span>
          <span style={{ fontSize: "24px", fontWeight: "bold" }}>Shop</span>
        </Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/category/:id" element={<Products />} />
        <Route path="/product/:id" element={<Product />} />
        <Route path="/search/:q" element={<Products />} />
      </Routes>
    </BrowserRouter>
  )

}

export default App