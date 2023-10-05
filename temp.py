digraph G {
    graph [rankdir=TB, size="10,10"]

    // Pre-production and Initial Preparation
    "Pre-Production" [shape=ellipse, fillcolor=lightyellow, style=filled];
    "Initial Preparation" [shape=ellipse, fillcolor=lightpink, style=filled];
    "Hull & Turret Divorce" [shape=box, label="Hull & Turret Divorce\n- Separation of Hull & Turret"];
    
    "Pre-Production" -> "Initial Preparation";
    "Initial Preparation" -> "Hull & Turret Divorce";

    subgraph cluster_0 {
        label = "Plant 1: Initial Operations & Fabrication";
        color = lightgrey;
        
        // Hull Operations in Plant 1
        "Hull Tear Down" [shape=box, label="Hull Tear Down\n- Divorce of Hull from Turret"];
        "Hull Appurtenance" [shape=box, label="Hull Appurtenance\n- Prepping Hull for Assembly Line"];
        "Hull Paint" [shape=box, label="Hull Shot Blast Painting\n- Rust removal from Hull"];
        
        "Hull & Turret Divorce" -> "Hull Tear Down";
        "Hull Tear Down" -> "Hull Appurtenance";
        "Hull Appurtenance" -> "Hull Paint";

        // Turret Operations in Plant 1
        "Remove Turr Rails and Appurt" [shape=box, label="Remove Turret Rails & Appurtenances\n- Preparation for Modifications"];
        "Turr Machine" [shape=box, label="Turret Machining\n- Prepping Turret for Armor Attachment"];
        "Turr Armor" [shape=box, label="Turret Armor Attachment\n- Adding Protective Armor"];
        "Turr Appurt" [shape=box, label="Turret Appurtenances Attachment\n- Adding necessary components"];
        "Turr Paint" [shape=box, label="Turret Shot Blast Painting\n- Rust removal from Turret"];
        
        "Hull & Turret Divorce" -> "Remove Turr Rails and Appurt";
        "Remove Turr Rails and Appurt" -> "Turr Machine";
        "Turr Machine" -> "Turr Armor";
        "Turr Armor" -> "Turr Appurt";
        "Turr Appurt" -> "Turr Paint";

        // Fabrication in Plant 1
        "Fabrication" [shape=ellipse, fillcolor=lightcyan, style=filled];
        "Cutting Operations" [shape=box, label="Cutting Operations\n- Laser, plasma, water jet cutting\n- Titanium alloy sheet cutting"];
        "Welding Operations" [shape=box, label="Welding Operations\n- Robotic & friction stir welding\n- Vehicle component fabrication"];
        
        "Initial Preparation" -> "Fabrication";
        "Fabrication" -> "Cutting Operations";
        "Fabrication" -> "Welding Operations";
    }

    subgraph cluster_1 {
        label = "Plant 3: Assembly Line";
        color = lightgrey;
        
        // Hull Assembly Line
        "Hull Assembly Line" [shape=box, fillcolor=lightcyan];
        "Hull Paint" -> "Hull Assembly Line";
        
        // Turret Assembly Line
        "Turr Assembly Line" [shape=box, fillcolor=lightcyan];
        "Turr Paint" -> "Turr Assembly Line";
        
        // Marriage & Final Assembly
        "Marriage & Final Assembly" [shape=ellipse, fillcolor=lightcoral, style=filled];
        "Hull Assembly Line" -> "Marriage & Final Assembly";
        "Turr Assembly Line" -> "Marriage & Final Assembly";
        "Fabrication" -> "Marriage & Final Assembly"; // Adding this line
    }

    subgraph cluster_2 {
        label = "Vehicle: Testing to Delivery";
        color = lightgrey;
        
        "Testing Phase" [shape=ellipse, fillcolor=lightgreen, style=filled];
        "Marriage & Final Assembly" -> "Testing Phase";
        
        // Testing Phase Sub-Nodes
        "QA & Inspection" [shape=box, label="QA & Inspection\n- Component Inspections\n- Fire Control System Calibration"];
        "Road Testing" [shape=box, label="Road Testing\n- Performance & Tolerance Tests"];
        "Final Acceptance Testing" [shape=box, label="Final Acceptance Testing\n- Over 1,200 Item Inspection"];
        "Testing Phase" -> "QA & Inspection";
        "Testing Phase" -> "Road Testing";
        "Testing Phase" -> "Final Acceptance Testing";
        
        "Final Delivery" [shape=ellipse, fillcolor=lightgray, style=filled];
        "QA & Inspection" -> "Final Delivery";
        "Road Testing" -> "Final Delivery";
        "Final Acceptance Testing" -> "Final Delivery";
    }
}
