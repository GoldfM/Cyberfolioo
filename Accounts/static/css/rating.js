class Rating {
  constructor(dom) {
    dom.innerHTML = '<svg width="110" height="20"></svg>';
    this.svg = dom.querySelector('svg');
    for(var i = 0; i < 5; i++)
      this.svg.innerHTML += `<polygon data-value="${i+1}"
           transform="translate(${i*22},0)"
           points="10,1 4,19.8 19,7.8 1,7.8 16,19.8" stroke-linejoin="round">`;
    this.svg.onclick = e => this.change(e);
    this.render();
  }

  change(e) {
    let value = e.target.dataset.value;
    value && (this.svg.parentNode.dataset.value = value);
    this.render();
  }

  render() {
    this.svg.querySelectorAll('polygon').forEach(star =>
    {
      let on = +this.svg.parentNode.dataset.value >= +star.dataset.value;
      star.classList.toggle('active', on);
    });
  }
}

document.querySelectorAll('.rating').forEach(dom => new Rating(dom));