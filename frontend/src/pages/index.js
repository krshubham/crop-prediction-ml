import React, {useState} from 'react';
import {cropImages} from "@/utils";

export default function Home() {
    const [selectedModel, setSelectedModel] = useState('');
    const [loading, setLoading] = useState(false);
    const [values, setValues] = useState({
        N: 50,
        P: 50,
        K: 50,
        ph: 50,
        temperature: 25,
        humidity: 50,
        rainfall: 20,
    });

    const handleModelChange = (e) => {
        setSelectedModel(e.target.value);
    };

    const handleSliderChange = (e, field) => {
        setValues({...values, [field]: parseInt(e.target.value, 10)});
    };


    const handleSubmit = async () => {
        try {
            setLoading(true);
            const response = await fetch(`http://localhost:8000/model/${selectedModel}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(values),
            });
            setLoading(false);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();

            // Handle the result as needed, for now, log it
            console.log('Prediction Result:', result.crop);

            // For demonstration, you can set a mock image URL for the prediction result
            setPredictionImage(cropImages[result.crop]);
        } catch (error) {
            setLoading(false);
            console.error('Error submitting the request:', error.message);
        } finally {
            setLoading(false);
        }
    };


    const [predictionImage, setPredictionImage] = useState(null);

    if (loading) {
        return (
            <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75 z-50">
                <div className="w-16 h-16 border-t-4 border-blue-500 border-solid rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="max-w-2xl w-full p-8 bg-white rounded shadow-md flex">
                <div className="flex-grow">
                    <h2 className="text-3xl font-semibold mb-6 text-center">Crop Prediction</h2>

                    <div className="mb-6">
                        <label htmlFor="model" className="block text-sm font-medium text-gray-600">
                            Select ML Model
                        </label>
                        <select
                            id="model"
                            name="model"
                            value={selectedModel}
                            onChange={handleModelChange}
                            className="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300 w-full"
                        >
                            <option value="">Select Model</option>
                            <option value="xgb">XGBoost</option>
                            <option value="lightgbm">LightGBM</option>
                            <option value="random_forest">Random Forest</option>
                            <option value="knn">KNN</option>
                            <option value="mlp">MLP</option>
                        </select>
                    </div>

                    <div className="space-y-4">
                        {Object.entries(values).map(([field, value]) => (
                            <div key={field}>
                                <label htmlFor={field} className="block text-sm font-medium text-gray-600">
                                    {field}{field === 'temperature' ? ' (°C) ' : ''}
                                </label>
                                <input
                                    type="range"
                                    id={field}
                                    name={field}
                                    min="0"
                                    max={field === 'ph' ? 14 : 300}
                                    value={value}
                                    onChange={(e) => handleSliderChange(e, field)}
                                    className="mt-1 w-full"
                                />
                                <span className="text-xs text-gray-500">{value}</span>
                            </div>
                        ))}
                    </div>

                    <div className="mt-6">
                        <button
                            type="button"
                            onClick={handleSubmit}
                            className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring focus:border-blue-300"
                        >
                            Predict
                        </button>
                    </div>
                </div>

                {predictionImage && (
                    <div className="ml-8">
                        <h2 className="text-3xl font-semibold mb-4">Prediction</h2>
                        <img src={predictionImage} alt="Prediction" className="rounded-lg shadow-md"/>
                    </div>
                )}
            </div>
        </div>

    );
}
