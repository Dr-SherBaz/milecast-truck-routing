export function ForecastSlider({
  value,
  onChange,
  disabled,
}: {
  value: number;
  onChange: (value: number) => void;
  disabled?: boolean;
}) {
  return (
    <div className="slider-block">
      <div className="slider-label">
        <label htmlFor="forecast">Corridor forecast window</label>
        <strong>+{value}h</strong>
      </div>
      <input
        id="forecast"
        type="range"
        min={0}
        max={48}
        step={1}
        value={value}
        disabled={disabled}
        onChange={(event) => onChange(Number(event.target.value))}
      />
      <div className="slider-scale">
        <span>Departure</span>
        <span>+24h</span>
        <span>+48h</span>
      </div>
      <p className="hint">
        Weather is sampled at each checkpoint ETA plus this offset. Moving the slider
        refreshes the corridor heatmap live.
      </p>
    </div>
  );
}
