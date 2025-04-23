import React, { useEffect, useState } from "react";
import axios from "axios";
import PersonIcon from "../Icons/PersonIcon";
import "./ProfileCard.css";

export default function ProfileCard({ onClose }) {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userId = sessionStorage.getItem("user_id");
        const role = sessionStorage.getItem("user_role");

        if (role === "student") {
          const res = await axios.get(`http://127.0.0.1:8000/get_student_info/${userId}`);
          setInfo(res.data);
        } else {
          setInfo({ error: "Only student info supported." });
        }
      } catch (err) {
        setInfo({ error: "Unable to fetch user info." });
      }
    };
    fetchData();
  }, []);

  return (
    <div className="profile-slide-card">
      <div className="profile-content">
        <button className="close-button" onClick={onClose}>✖</button>
        <div className="profile-icon-center">
          <PersonIcon />
        </div>
        <h3 className="profile-heading">Personal Info</h3>
        {info?.error ? (
          <p>{info.error}</p>
        ) : info ? (
          <div className="profile-details">
            <p><strong>Name:</strong> {info.name}</p>
            <p><strong>Email:</strong> {info.email}</p>
            <p><strong>ID:</strong> {info.id_number}</p>
            <p><strong>Emergency:</strong> {info.emergency_contact}</p>
            <p><strong>Address:</strong> {info.personal_address}</p>
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </div>
    </div>
  );
}
