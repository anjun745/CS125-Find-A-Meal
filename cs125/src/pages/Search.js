import {useState} from "react";


export default function Search(){
    const [query, setQuery] = useState("");
    const [serverValue, setServerValue] = useState("");
    const [caloriesFilter, setCaloriesFilter] = useState(false);
    const [macrosFilter, setMacrosFilter] = useState(false);

    async function search(){
        const res = await fetch(`http://127.0.0.1:5000/api/search`,{ //?q=${query}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({query: query, filters: {
                calories: caloriesFilter,
                macros: macrosFilter
            }})
        });
        const data = await res.json();
        setServerValue(data.data); //sends body to server on localhost:5000/api/search
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
            <form id="filter-search">
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
            </form>
            <button type="submit">Search</button>
            <p>Server Response: {JSON.stringify(serverValue, null, 2)}</p>
        </div>
        </form>
    );
}