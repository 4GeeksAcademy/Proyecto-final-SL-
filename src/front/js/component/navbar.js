import React from "react";
import { Link } from "react-router-dom";

export const Navbar = () => {

	const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/');
    };

	#esta funcion ira en login, hay que llamar al endpoint, añadir useeffect con terciario 
	const handleLogin = async () => {
		const response = fetch(`${URL}/login`,{method:"POST",headers:{'Content-Type:application/json'} ,body:JSON.stringify({email:email, password:password})})
		const data = await response.json()

		if (data.access_token) {
			localStorage.setItem("token", data.access_token)
			navigate('/user');
		}

    };
	return (
		<nav className="navbar p-3 m-3" style={{ backgroundColor: 'rgba(0, 0, 0, 0.8)' }}>
			<div className="container">
				<Link to="/">
				<button className="btn btn-secondary">Classified photos</button>
				</Link>
				<div className="ml-auto">
					<Link to="/demo">
						<button className="btn btn-secondary">Photos uploaded</button>
					</Link>
				</div>
				<button className="btn btn-warning btn-lg" onClick={handleLogout}>
                    Logout
                </button>
			</div>
		</nav>
	);
};
