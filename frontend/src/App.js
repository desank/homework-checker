import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
    const [results, setResults] = useState(null);
    const [error, setError] = useState('');

    const handleFileChange = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post('http://localhost:8000/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setResults(response.data);
            setError('');
        } catch (err) {
            setError('Error processing the image. Please try again.');
            setResults(null);
        }
    };

    return (
        <div className="container mt-5">
            <h1 className="text-center mb-4">Math Homework Checker</h1>
            <div className="card">
                <div className="card-body">
                    <div className="mb-3">
                        <label htmlFor="formFile" className="form-label">Upload a picture of the homework</label>
                        <input className="form-control" type="file" id="formFile" accept="image/*" onChange={handleFileChange} />
                    </div>
                </div>
            </div>

            {error && <div className="alert alert-danger mt-4">{error}</div>}

            {results && (
                <div className="mt-4">
                    <h2>Results</h2>
                    <p>{results.correct_count} / {results.total_count} correct</p>
                    <ul className="list-group">
                        {results.results.map((result, index) => (
                            <li key={index} className={`list-group-item ${
                                result.is_correct ? 'list-group-item-success' : 'list-group-item-danger'
                            }`}>
                                {result.expression}
                                {!result.is_correct && (
                                    <span className="badge bg-danger ms-2">Correct Answer: {result.correct_answer}</span>
                                )}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default App;