// Navbar scroll
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
});

// Hamburger
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
hamburger.addEventListener('click', () => navLinks.classList.toggle('open'));
document.querySelectorAll('.nav-links a').forEach(a => {
  a.addEventListener('click', () => navLinks.classList.remove('open'));
});

// Skill bars on scroll
const bars = document.querySelectorAll('.skill-bar');
const skillObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.width = e.target.dataset.w + '%';
      skillObs.unobserve(e.target);
    }
  });
}, { threshold: 0.4 });
bars.forEach(b => skillObs.observe(b));

// Fade-in on scroll
const fadeEls = document.querySelectorAll('.skill-card, .svc-card, .work-card, .contact-row');
const fadeObs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.opacity = '1';
      e.target.style.transform = 'translateY(0)';
      fadeObs.unobserve(e.target);
    }
  });
}, { threshold: 0.15 });
fadeEls.forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(24px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  fadeObs.observe(el);
});

// Contact form
function handleSubmit(e) {
  e.preventDefault();
  const btn = e.target.querySelector('button');
  const orig = btn.innerHTML;
  btn.innerHTML = '<i class="fas fa-check"></i> Sent!';
  btn.style.background = '#22c55e';
  btn.style.color = '#fff';
  setTimeout(() => {
    btn.innerHTML = orig;
    btn.style.background = '';
    btn.style.color = '';
    e.target.reset();
  }, 3000);
}
fetch("/api/contact", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
});