import React, { useState } from "react";

const Register = () => {
  const [formData, setFormData] = useState({
    username: "",
    firstname: "",
    lastname: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRegister = async () => {
    const response = await fetch("/djangoapp/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });
    const data = await response.json();
    if (data.status === "Authenticated") {
      setMessage("Registration successful!");
    } else {
      setMessage("Registration failed. Try again.");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "50px auto" }}>
      <h2>Sign Up</h2>
      {message && <p>{message}</p>}
      <input
        name="username"
        placeholder="Username"
        onChange={handleChange}
        style={{ display: "block", margin: "10px 0", width: "100%" }}
      />
      <input
        name="firstname"
        placeholder="First Name"
        onChange={handleChange}
        style={{ display: "block", margin: "10px 0", width: "100%" }}
      />
      <input
        name="lastname"
        placeholder="Last Name"
        onChange={handleChange}
        style={{ display: "block", margin: "10px 0", width: "100%" }}
      />
      <input
        name="email"
        placeholder="Email"
        type="email"
        onChange={handleChange}
        style={{ display: "block", margin: "10px 0", width: "100%" }}
      />
      <input
        name="password"
        placeholder="Password"
        type="password"
        onChange={handleChange}
        style={{ display: "block", margin: "10px 0", width: "100%" }}
      />
      <button
        onClick={handleRegister}
        style={{ marginTop: "10px", padding: "10px 20px" }}
      >
        Register
      </button>
    </div>
  );
};

export default Register;