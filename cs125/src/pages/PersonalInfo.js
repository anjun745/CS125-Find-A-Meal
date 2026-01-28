import {useState, useEffect} from "react";

export default function PersonalInfo(){
    const [height, setHeight] = useState("");
    const[weight, setWeight] = useState("");
    const[age, setAge] = useState("");
    const [serverValue, setServerValue] = useState({ height: "", weight: "", age: "", gender: ""});
    const[gender, setGender] = useState("");
    const genders = [
        {value: 0, label: 'Female'},
        {value:  1, label: 'Male'}
    ];

    useEffect(() => {
        fetch("http://localhost:5000/api/info")
        .then((res) => res.json())
        
    .catch(() => setServerValue("(failed to load)"));
    }, []);

    async function saveAll(){
        const res = await fetch("http://localhost:5000/api/info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({gender,
                                height: height === "" ? null : parseInt(height),
                                weight: weight === "" ? null : parseInt(weight),
                                age: age === "" ? null : parseInt(age)}),
        });
        const data = await res.json();
        setServerValue(data.data); //expects {height, weight, age, gender }
    }

    return(
        <div className="user-container">
            <h2>Personal Info</h2>
            <div>
                {genders.map((g) => (
                    <label key={g.value}>
                    <input
                        type="radio"
                        name="gender"
                        value={g.value}
                        checked={gender === g.value}
                        onChange={() => setGender(g.value)}
                    />
                    {g.label}
                    </label>
                ))}
            </div>
            <input
                placeholder="Enter Height (cm)"
                value={height}
                onChange={(e) => setHeight(e.target.value)}
            />

            <input
                placeholder="Enter Weight (lbs)"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
            />

            <input
                placeholder="Enter Age"
                value={age}
                onChange={(e) => setAge(e.target.value)}
            />
            
            <button onClick={saveAll} style={{ marginLeft: 8 }}>
                Save
            </button>

            <p>Saved on server: {JSON.stringify(serverValue, null, 2)}</p>
        </div>
    );
}