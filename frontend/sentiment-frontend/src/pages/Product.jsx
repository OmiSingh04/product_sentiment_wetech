import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"
import "./Product.css"

function Product() {
  const { id } = useParams()
  const [product, setProduct] = useState(null)
  const [reviews, setReviews] = useState([])
  const [sentiment, setSentiment] = useState(null)

  const [newComment, setNewComment] = useState("")
  const [newRating, setNewRating] = useState(5)

  useEffect(() => {
    // Fetch product details
    fetch(`http://localhost:5000/api/products/${id}`)
      .then(r => r.json())
      .then(setProduct)

    // Fetch reviews
    fetch(`http://localhost:5000/api/products/${id}/reviews`)
      .then(r => r.json())
      .then(setReviews)

    // Fetch overall sentiment
    fetch(`http://localhost:5000/api/products/${id}/sentiment`)
      .then(r => {
        if (r.status === 404) return null
        return r.json()
      })
      .then(setSentiment)
  }, [id])

  if (!product) return <div>LOADING...</div>


  const submitReview = () => {
    fetch("http://localhost:5000/add_review", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
        product_id: Number(id),
        rating: newRating,
        comment: newComment
        })
    })
    .then(() => {
        setNewComment("")
        setNewRating(5)

        // reload reviews
        return fetch(`http://localhost:5000/api/products/${id}/reviews`)
    })
    .then(r => r.json())
    .then(setReviews)
  }


  return (
    <div className="product-container">
      <h1 className="product-title">Product: {product.name}</h1>
      <h2 className="product-title">Description: {product.description}</h2>
      <h2 className="product-title">Price: {product.price}</h2>

      {/* SENTIMENT SUMMARY */}
      {sentiment && (
        <div 
          style={{
            marginTop: "20px",
            padding: "10px",
            border: "1px solid #ccc",
            borderRadius: "8px",
            backgroundColor: "#eef6ff"
          }}
        >
          <strong>Overall Sentiment:</strong> {sentiment.overall_sentiment}
        </div>
      )}

      {/* REVIEWS PANEL */}
      {reviews.length > 0 && (
        <div 
          style={{
            border: "1px solid #ccc",
            borderRadius: "8px",
            padding: "10px",
            maxHeight: "300px",
            overflowY: "auto",
            backgroundColor: "#f9f9f9",
            marginTop: "10px"
          }}
        >
          <h3 style={{ marginBottom: "10px" }}>Reviews</h3>
          
          {reviews.map((r, i) => (
            <div 
              key={i} 
              style={{
                display: "flex",
                alignItems: "flex-start",
                gap: "10px",
                backgroundColor: "#fff",
                padding: "10px",
                marginBottom: "10px",
                borderRadius: "8px",
                boxShadow: "0 1px 4px rgba(0,0,0,0.15)",
                maxWidth: "fit-content"
              }}
            >
              {/* User circle */}
              <div style={{
                width: "40px",
                height: "40px",
                borderRadius: "50%",
                backgroundColor: "#ddd",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontWeight: "bold",
                color: "#555",
                flexShrink: 0
              }}>
                👤
              </div>

              {/* Comment content */}
              <div style={{ flex: 1 }}>
                {/* STAR RATING */}
                <div style={{ marginBottom: "5px" }}>
                  {"★".repeat(r.rating) + "☆".repeat(5 - r.rating)}
                </div>

                {/* COMMENT */}
                <div>
                  {r.comment}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}


    <div className="review-form">
        <h3>Write a Review</h3>

        {/* STAR SELECT */}
        <select
            value={newRating}
            onChange={e => setNewRating(Number(e.target.value))}
        >
            {[1,2,3,4,5].map(n => (
            <option key={n} value={n}>{n} Star{n > 1 && "s"}</option>
            ))}
        </select>

        {/* COMMENT BOX */}
        <textarea
            placeholder="Write your review"
            value={newComment}
            onChange={e => setNewComment(e.target.value)}
            rows={4}
        />

        <button onClick={submitReview}>
            Submit Review
        </button>
    </div>


    </div>
  )
}

export default Product
