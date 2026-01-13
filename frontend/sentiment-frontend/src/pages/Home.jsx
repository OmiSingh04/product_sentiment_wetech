import { useNavigate } from "react-router-dom"
import { useEffect, useState } from "react"
import "./Home.css"


function Home() {
  const [categories, setCategories] = useState([])
  const navigate = useNavigate()

  const [query, setQuery] = useState("")

  useEffect(() => {
    fetch("http://localhost:5000/api/categories")
      .then(res => res.json())
      .then(data => setCategories(data))
  }, [])

  return (
    <div className="home-container">
      <input
        className="search-bar"
        placeholder="Search products..."
        value = {query}
        onChange={e => setQuery(e.target.value)}
        onKeyDown={e => {
            if(e.key === "Enter") navigate(`/search/${query}`)
        }}
        style={{ width: "100%", padding: "10px", marginBottom: "20px" }}
      />

      <h1>Categories</h1>

      <div className="category-grid" style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "20px" }}>

        {categories.map(cat => (
          <div className="category-card" key={cat.id} onClick={() => navigate(`/category/${cat.id}`)}
                style={{ cursor: "pointer", border: "1px solid #ccc", padding: "20px" }} >
                {cat.name}
          </div>
        ))}

      </div>
    </ div>
  )
}

export default Home