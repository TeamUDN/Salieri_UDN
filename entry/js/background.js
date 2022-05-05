bubbly({
  colorStart: '#331e00',
  colorStop: '#331e00',
  blur: 5,
  bubbles: 80,
  velocityFunc: () => Math.random() * 2.5,
  radiusFunc: () => Math.random() * 15,
  bubbleFunc: () => `hsla(0, 80%, 40%, ${Math.random() * 0.3})`
});
