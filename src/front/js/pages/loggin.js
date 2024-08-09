import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Context } from '../store/appContext';

const loggin = () => {
    const {actions} = useContext(Context)
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLoggin = async (e) => {
        e.preventDefault()
        const logged = await actions.loggin(email, password)

        if (logged){
            navigate("/home");
        }
    }

    return (
        <div className="loggin-container">
            <form onSubmit={handleLoggin}>
                <div>
                    <label htmlFor="email">Email:</label>
                    <input
                        type="text"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit">loggin</button>
                <Link to="/">
				    <span className="btn btn-primary btn-lg" href="#" role="button">
					    Register
				    </span>
			    </Link>
            </form>
        </div>
    );
};

export default loggin;