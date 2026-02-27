import {useEffect, useState} from "react";


export default function Home(){
    const [results, setResults] = useState([]);
    const [mealType, setMealType] = useState("");

    useEffect(() => {
    async function home(){
        const res = await fetch(`http://127.0.0.1:5000/api/home`);
        const data = await res.json();
        setMealType(data.meal_type ?? ""); 
        setResults(data.meals ?? []);
    }
    home();
    }, []);
    function capitalize(word){
        if (!word) return "";
        return word.charAt(0).toUpperCase() + word.slice(1);
    }

    return(
    <>
    <h2>Welcome, it's {capitalize(mealType)} Time 😋🍴</h2>
        <div className="results">
            {results.length === 0 && <p>No results </p>}
            {results.map((recipe) => (
                <div key={recipe.id} className="recipe-card">
                    <h3>{recipe.title}</h3>
                    <img
                        src={recipe.image_url}
                        alt={recipe.title}
                        width="200"
                    />
                    <p>Calories: {recipe.calories != null ? Math.round(recipe.calories) : "N/A"} kcal</p>
                    <p>Ready in {recipe.ready_in_minutes ?? "?"} minutes</p>
                    <a href={recipe.source_url} target="_blank" rel="noreferrer">
                        View Recipe
                    </a>
                </div>
                ))}
        </div>
    </>
    );
}