import {useState} from "react";
import "./Search.css";


export default function Search(){
    const [query, setQuery] = useState("");
    const [caloriesFilter, setCaloriesFilter] = useState(false);
    const [macrosFilter, setMacrosFilter] = useState(false);
    const [results, setResults] = useState([]);

    async function search(){
        const res = await fetch(`http://127.0.0.1:5000/api/search`,{ 
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({query: query, filters: {
                calories: caloriesFilter,
                macros: macrosFilter
            }})
        });
        const data = await res.json();
        console.log(data.meals);
        setResults(data.meals ?? []);
    }

    return(
        <form
            onSubmit={(e) => {
                e.preventDefault();
                search();
            }}
        >
        <div className="search-container">
            <h2>Search</h2>
            <p>Enter ingredients, with commas separating each ingredient</p>
            <input
                type="text"
                placeholder="Search by ingredients..."
                value={query}
                required
                onChange={(e) => setQuery(e.target.value)}
            />
            <div id="filter-search">
                <p>Filter Results By</p>
                <div>
                    <label>
                        <input type="checkbox" name="calories" value="calories"
                        checked={caloriesFilter}
                        onChange={(e) => setCaloriesFilter(e.target.checked)}
                        />
                        Recommended Calories
                    </label>
                </div>
                <label>
                    <input type="checkbox" name="macros" value="macros"
                    checked={macrosFilter}
                    onChange={(e) => setMacrosFilter(e.target.checked)}
                    />
                    Macro Restrictions
                </label>
            </div>
            <button type="submit">Search</button>
        </div>
        
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
        </form>

    );
}