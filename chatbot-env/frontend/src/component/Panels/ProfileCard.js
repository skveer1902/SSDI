import React, { useEffect, useState } from "react";
import axios from "axios";
import "./ProfileCard.css";

function ProfileCard({ onClose }) {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");

  const userId = sessionStorage.getItem("user_id");
  const userRole = sessionStorage.getItem("user_role");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        let endpoint = "";

        if (userRole === "student") {
          endpoint = `/get_student_info/${userId}`;
        } else if (userRole === "faculty") {
          endpoint = `/faculty/get_info/${userId}`;
        } else if (userRole === "admin") {
          endpoint = `/admin/get_info/${userId}`;
        } else {
          throw new Error("Invalid role");
        }

        const res = await axios.get(`http://127.0.0.1:8000${endpoint}`);
        setProfile(res.data);
      } catch (error) {
        console.error("Failed to fetch profile info:", error);
        setError("Failed to load profile information.");
      }
    };

    fetchProfile();
  }, [userRole, userId]);

  // Fields you want to show
  const displayFields = ["name", "email", "emergency_contact", "personal_address"];

  return (
    <div className="profile-slide-card">
      <div className="profile-content">
        <button className="close-button" onClick={onClose}>✖</button>

        <div className="profile-icon-center">
          <div className="person-icon">
            <div className="head" />
            <div className="body" />
          </div>
        </div>

        <h3 className="profile-heading">Personal Info</h3>

        <div className="profile-details">
          {error ? (
            <p className="error-message">{error}</p>
          ) : profile ? (
            displayFields.map((field) => (
              profile[field] && (
                <p key={field}>
                  <strong>{field.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}:</strong> {profile[field]}
                </p>
              )
            ))
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>

      {/* Backdrop Area */}
      <div className="profile-backdrop" onClick={onClose} />
    </div>
  );
}

export default ProfileCard;
