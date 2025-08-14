// frontend/src/pages/Home.jsx
import React from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

// Importing local images
import img1 from "../images/1.jpg";
import img2 from "../images/2.jpg";
import img3 from "../images/3.jpg";
import teamworkImg from "../images/teamwork.jpg";
import person1 from "../images/person1.jpg";
import person2 from "../images/person2.jpg";
import person3 from "../images/person3.jpg";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Home = () => {
  return (
    <div>
      <Navbar />
      

      {/* HERO SECTION */}
      <section
        className="text-center text-white d-flex align-items-center justify-content-center"
        style={{
          background: "linear-gradient(135deg, #6a11cb 0%, #2575fc 100%)",
          height: "100vh",
        }}
      >
        <div>
          <h1 className="display-3 fw-bold">Welcome to IdeaReview Hub</h1>
          <p className="lead mt-3">
            Share your brilliant ideas, get them reviewed, and make them shine!
          </p>
          <div className="mt-4">
            <Link to="/signup" className="btn btn-light btn-lg me-3">
              🚀 Get Started
            </Link>
            <Link to="/login" className="btn btn-outline-light btn-lg">
              🔑 Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* CAROUSEL */}
      <section className="py-5 bg-light">
        <div className="container">
          <h2 className="text-center mb-4">Explore Creative Ideas</h2>
          <div
            id="ideaCarousel"
            className="carousel slide"
            data-bs-ride="carousel"
            data-bs-interval="3000"
          >
            <div className="carousel-inner">
              <div className="carousel-item active">
                <img
                  src={img1}
                  className="d-block w-100 rounded"
                  alt="Idea 1"
                  style={{ height: "400px", objectFit: "cover" }}
                />
              </div>
              <div className="carousel-item">
                <img
                  src={img2}
                  className="d-block w-100 rounded"
                  alt="Idea 2"
                  style={{ height: "400px", objectFit: "cover" }}
                />
              </div>
              <div className="carousel-item">
                <img
                  src={img3}
                  className="d-block w-100 rounded"
                  alt="Idea 3"
                  style={{ height: "400px", objectFit: "cover" }}
                />
              </div>
            </div>
            <button
              className="carousel-control-prev"
              type="button"
              data-bs-target="#ideaCarousel"
              data-bs-slide="prev"
            >
              <span className="carousel-control-prev-icon"></span>
            </button>
            <button
              className="carousel-control-next"
              type="button"
              data-bs-target="#ideaCarousel"
              data-bs-slide="next"
            >
              <span className="carousel-control-next-icon"></span>
            </button>
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-5 bg-white">
        <div className="container">
          <h2 className="text-center mb-5">How It Works</h2>
          <div className="row g-4 text-center">
            <div className="col-md-4">
              <div className="p-4 shadow-sm rounded bg-light">
                <h3>📝 Submit</h3>
                <p>Share your idea with a detailed description and images.</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-4 shadow-sm rounded bg-light">
                <h3>🔍 Review</h3>
                <p>Our community and admins provide constructive feedback.</p>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-4 shadow-sm rounded bg-light">
                <h3>🚀 Launch</h3>
                <p>Collaborate and turn your idea into a real-world success.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* TESTIMONIALS */}
      <section
        className="py-5 text-white"
        style={{ backgroundColor: "#1f1f1f" }}
      >
        <div className="container">
          <h2 className="text-center mb-5">What Our Members Say</h2>
          <div className="row g-4">
            {[{ name: "Jane Doe", text: "My business grew by 200% thanks to this platform!", img: person1 },
              { name: "John Smith", text: "Professional, efficient, and inspiring community.", img: person2 },
              { name: "Sarah Lee", text: "Helped me refine my idea into a real product.", img: person3 }
            ].map((t, i) => (
              <div className="col-md-4" key={i}>
                <div className="p-4 bg-dark rounded shadow-sm text-center h-100">
                  <img
                    src={t.img}
                    alt={t.name}
                    className="rounded-circle mb-3"
                    style={{ width: "80px", height: "80px", objectFit: "cover" }}
                  />
                  <p>"{t.text}"</p>
                  <h5 className="mt-3">{t.name}</h5>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CALL TO ACTION */}
      <section
        className="py-5 text-white"
        style={{ backgroundColor: "#2575fc" }}
      >
        <div className="container text-center">
          <h2>Have an Idea That Can Change the World?</h2>
          <p className="lead mb-4">
            Don’t keep it to yourself. Share it, get feedback, and make it
            happen!
          </p>
          <Link to="/signup" className="btn btn-light btn-lg">
            🚀 Start Now
          </Link>
        </div>
      </section>

      {/* CONTACT US */}
      <section id="contact" className="py-5 bg-light">
        <div className="container">
          <h2 className="text-center mb-4">Contact Us</h2>
          <form className="mx-auto" style={{ maxWidth: "500px" }}>
            <div className="mb-3">
              <label className="form-label">Name</label>
              <input
                type="text"
                className="form-control"
                placeholder="Your name"
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                placeholder="Your email"
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Message</label>
              <textarea
                className="form-control"
                rows="4"
                placeholder="Your message"
              ></textarea>
            </div>
            <button type="submit" className="btn btn-primary w-100">
              Send Message
            </button>
          </form>
        </div>
      </section>

     
  <Footer />
    </div>
  );
};

export default Home;
