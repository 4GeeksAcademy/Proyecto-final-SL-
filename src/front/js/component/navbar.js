import React from "react";
import { Link } from "react-router-dom";
import beBananaLogo from "../img/BeBanana.png";

export const Navbar = () => {

	const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/');
    };

	return (
		<nav className="navbar p-3 m-3" style={{ backgroundColor: 'rgba(46, 39, 1, 0.8)' }}>
			<div className="container">
				<Link to="/">
					<img src={beBananaLogo} alt="Be Banana Logo" style={{ height: "75px" }} className="navbar-logo mb-0 h1" />
				</Link>
				<div className="ml-auto">
					<Link to="/demo">
						<button className="btn btn-secondary">Photos uploaded</button>
					</Link>
				</div>
				<button className="btn btn-warning btn-lg" onClick={handleLogout}>Logout</button>
			</div>
		</nav>
	);
};
