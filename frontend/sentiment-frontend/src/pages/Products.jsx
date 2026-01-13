import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import "./Products.css"

function Products() {
  const { id, q } = useParams()
  const [products, setProducts] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    const url = q ? `http://localhost:5000/api/products/search?q=${q}` : `http://localhost:5000/api/products?category_id=${id}`
    fetch(url) .then(res => res.json()) .then(setProducts)
  }, [id, q])

  return (
    <div className="products-container">
      <h2>{q ? `Search: ${q}` : "Products"}</h2>

      <div className="product-list">
          {products.map(p => (
            <div key={p.id} className="product-item"
            onClick={() => navigate(`/product/${p.id}`)}
            style={{cursor: "pointer"}}
            >
              {p.name} 
            </div>
            ))
          }
      </div>

    </ div>
  )
}

export default Products
