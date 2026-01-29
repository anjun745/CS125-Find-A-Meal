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
    const[fitness, setFitness] = useState("");
    const fitness_goals = [
        {value: 0, label: 'Weight Loss'},
        {value: 1, label: 'Maintain Current Weight'},
        {value: 2, label: 'Weight Gain'}
    ]
    useEffect(() => {
        fetch("http://localhost:5000/api/info")
        .then((res) => res.json())
        
    .catch(() => setServerValue("(failed to load)"));
    }, []);

    async function saveAll(){
        const res = await fetch("http://localhost:5000/api/info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({gender, fitness,
                                height: height === "" ? null : parseInt(height),
                                weight: weight === "" ? null : parseInt(weight),
                                age: age === "" ? null : parseInt(age)}),
        });
        const data = await res.json();
        setServerValue(data.data); //sends body to server on localhost:5000/api/info
    }

    return(
        <div className="user-container">
            <h2>Personal Info</h2>
            <p>Pick your Gender</p>
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
            <p> Submitting your height, weight, and age will result in most accurate recommendations</p>
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
            <p>Pick your Weight Goal</p>
            <div>
                {fitness_goals.map((f) => (
                    <label key={f.value}>
                    <input
                        type="radio"
                        name="fitness"
                        value={f.value}
                        checked={fitness === f.value}
                        onChange={() => setFitness(f.value)}
                    />
                    {f.label}
                    </label>
                ))}
            </div>
            
            <button onClick={saveAll} style={{ marginLeft: 8 }}>
                Save
            </button>

            <p>Saved on server: {JSON.stringify(serverValue, null, 2)}</p>
        </div>
    );
}