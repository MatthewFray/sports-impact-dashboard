import { useEffect, useState } from "react";

type ImpactMetric = {
  label: string;
  value: number;
};

type PlayerImpactResponse = {
  player_id: number;
  player_name: string;
  metrics: ImpactMetric[];
  metadata: {
    model_version: string;
    uses_ml: boolean;
  };
};

function PlayerImpact() {
  const [playerImpact, setPlayerImpact] = useState<PlayerImpactResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchPlayerImpact() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch("http://localhost:8000/players/1/impact");
        if (!response.ok) {
          throw new Error("Failed to load player impact data.");
        }

        const data: PlayerImpactResponse = await response.json();
        setPlayerImpact(data);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("Something went wrong while fetching player impact data.");
        }
      } finally {
        setLoading(false);
      }
    }

    fetchPlayerImpact();
  }, []);

  if (loading) {
    return <div>Loading player impact data...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!playerImpact) {
    return <div>No player impact data found.</div>;
  }

  return (
    <div>
      <h2>{playerImpact.player_name}</h2>

      <div>
        {playerImpact.metrics.map((metric) => (
          <div
            key={metric.label}
            style={{
              border: "1px solid #ccc",
              padding: "12px",
              marginBottom: "8px",
            }}
          >
            <div>{metric.label}</div>
            <div>{metric.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PlayerImpact;
