import pulp

def optimize_dispatch(tickets: list, technicians: list) -> dict:
    """
    Uses Linear Programming to optimally assign high-priority tickets 
    to available CCS technicians without exceeding their shift capacities.
    """
    
    # 1. Initialize the Optimization Problem (Maximization)
    prob = pulp.LpProblem("ITSM_Ticket_Assignment", pulp.LpMaximize)
    
    # 2. Define the Decision Variables
    # Creates a dictionary of binary variables (0 or 1) for every ticket-technician pair
    x = pulp.LpVariable.dicts(
        "assign", 
        ((t['id'], tech['id']) for t in tickets for tech in technicians),
        cat='Binary'
    )
    
    # 3. Define the Objective Function
    # We want to maximize the sum of (Priority Score * Assignment)
    prob += pulp.lpSum(
        tickets[i]['priority'] * x[(tickets[i]['id'], technicians[j]['id'])]
        for i in range(len(tickets)) for j in range(len(technicians))
    ), "Maximize_Priority_Resolution"
    
    # 4. Define Constraints
    
    # Constraint A: Each ticket is assigned to AT MOST one technician
    for t in tickets:
        prob += pulp.lpSum(x[(t['id'], tech['id'])] for tech in technicians) <= 1, f"Max_One_Tech_per_Ticket_{t['id']}"
        
    # Constraint B: Technicians cannot exceed their available working hours
    for tech in technicians:
        prob += pulp.lpSum(
            tickets[i]['time_required'] * x[(tickets[i]['id'], tech['id'])] 
            for i in range(len(tickets))
        ) <= tech['capacity'], f"Capacity_Limit_{tech['id']}"
        
    # 5. Solve the Problem
    prob.solve()
    
    # 6. Parse and Return the Results
    assignments = []
    for t in tickets:
        for tech in technicians:
            if pulp.value(x[(t['id'], tech['id'])]) == 1.0:
                assignments.append({
                    "ticket_id": t['id'],
                    "technician_id": tech['id'],
                    "priority_handled": t['priority']
                })
                
    return {
        "status": pulp.LpStatus[prob.status],
        "total_priority_resolved": pulp.value(prob.objective),
        "assignments": assignments
    }

# --- TEST THE ALGORITHM ---
if __name__ == "__main__":
    # Mock Open Tickets (From your AI Triage)
    # Time is in hours
    mock_tickets = [
        {"id": "TKT-101", "priority": 9, "time_required": 2}, # High priority, quick fix
        {"id": "TKT-102", "priority": 4, "time_required": 4}, # Low priority, takes long
        {"id": "TKT-103", "priority": 8, "time_required": 1}, # High priority, very quick
    ]
    
    # Mock Available Technicians (From your Resource Logs)
    # Capacity is in hours
    mock_technicians = [
        {"id": "TECH-Juan", "capacity": 3},
        {"id": "TECH-Maria", "capacity": 2},
    ]
    
    results = optimize_dispatch(mock_tickets, mock_technicians)
    print("Optimization Status:", results["status"])
    print("Assignments:", results["assignments"])