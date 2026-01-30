import {useState, useEffect} from "react";

export default function PersonalInfo(){
    const [height, setHeight] = useState("");
    const[weight, setWeight] = useState("");
    const[age, setAge] = useState("");
    const [serverValue, setServerValue] = useState(""); //to verify what is saved
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
    const[activity, setActivity] = useState("");
    const activity_level = [
        {value: 1.2, label: 'Sedentary (little/no exercise)'},
        {value: 1.375, label: 'Lightly active (light exercise 1–3 days/week)'},
        {value: 1.55, label: 'Moderately active (moderate exercise 3–5 days/week)'},
        {value: 1.725, label: 'Very active (hard exercise 6–7 days/week)'},
        {value: 1.9, label: 'Extremely active (very hard training / job)'}
    ]
    const [macros, setMacros] = useState({
        protein: "",
        carbs: "",
        fat: "",
        fiber: "",
        sugarLimit: "",
        allergies: ""
    });
    const { protein, carbs, fat, fiber, sugarLimit, allergies } = macros;

    async function saveAll(){
        const res = await fetch("http://localhost:5000/api/info", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({gender, fitness, activity, 
        macros:{
            protein: protein === "" ? null : parseInt(protein),
            carbs: carbs === "" ? null : parseInt(carbs),
            fat: fat === "" ? null : parseInt(fat),
            fiber: fiber === "" ? null : parseInt(fiber),
            sugarLimit: sugarLimit === "" ? null : parseInt(sugarLimit),
            allergies
        },
            height: height === "" ? null : parseInt(height),
            weight: weight === "" ? null : parseInt(weight),
            age: age === "" ? null : parseInt(age)})
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
                type="number"
                onChange={(e) => setHeight(e.target.value)}
            />

            <input
                placeholder="Enter Weight (lbs)"
                value={weight}
                type="number"
                onChange={(e) => setWeight(e.target.value)}
            />

            <input
                placeholder="Enter Age"
                value={age}
                type="number"
                onChange={(e) => setAge(e.target.value)}
            />

            <p>Choose your Activity Level</p>
            <div>
                {activity_level.map((a) => (
                    <div key={a.value}>
                        <label key={a.value}>
                        <input
                            type="radio"
                            name="activity"
                            value={a.value}
                            checked={activity === a.value}
                            onChange={() => setActivity(a.value)}
                        />
                        {a.label}
                        </label>
                    </div>
                ))}
            </div>

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

            <p>Macro Goals & Food Restrictions</p>
            <div>
            <div>
                <label>
                    Protein (g/day)
                    <input
                    type="number"
                    value={macros.protein}
                    onChange={(e) => setMacros({ ...macros, protein: e.target.value })}
                    />
                </label>
                <label>
                    Carbs (g/day)
                    <input
                    type="number"
                    value={macros.carbs}
                    onChange={(e) => setMacros({ ...macros, carbs: e.target.value })}
                    />
                </label>
            </div>

            <div>
                <label>
                    Fat (g/day)
                    <input
                    type="number"
                    value={macros.fat}
                    onChange={(e) => setMacros({ ...macros, fat: e.target.value })}
                    />
                </label>

                <label>
                    Fiber target (g/day)
                    <input
                    type="number"
                    value={macros.fiber}
                    onChange={(e) => setMacros({ ...macros, fiber: e.target.value })}
                    />
                </label>
            </div>

            <label>
                Sugar limit (g/day)
                <input
                type="number"
                value={macros.sugarLimit}
                onChange={(e) => setMacros({ ...macros, sugarLimit: e.target.value })}
                />
            </label>

            <label>
                Allergies (comma-separated)
                <input
                type="text"
                placeholder="e.g., peanuts, shellfish"
                value={macros.allergies}
                onChange={(e) => setMacros({ ...macros, allergies: e.target.value })}
                />
            </label>
            </div>
            
            <button onClick={saveAll} style={{ marginLeft: 8 }}>
                Save
            </button>

            <p>Saved on server: {JSON.stringify(serverValue, null, 2)}</p>
        </div>
    );
}