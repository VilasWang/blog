/* 自定义背景和视觉效果 JavaScript */

document.addEventListener('DOMContentLoaded', function() {

  // 鼠标点击涟漪效果
  initRippleEffect();

  // 科技感鼠标跟随效果
  initTechCursorEffect();

  // 粒子效果
  if (butterfly_config.visual_effects && butterfly_config.visual_effects.particles.enable) {
    initParticles();
  }

  // 星空效果
  if (butterfly_config.visual_effects && butterfly_config.visual_effects.starry_sky.enable) {
    initStarrySky();
  }

  // 打字机效果
  if (butterfly_config.typewriter && butterfly_config.typewriter.enable) {
    initTypewriter();
  }

  // 动态渐变背景
  initAnimatedBackground();

  // 霓虹文字效果
  initNeonGlow();
});

// 鼠标点击涟漪效果
function initRippleEffect() {
  document.addEventListener('click', function(e) {
    if (!butterfly_config.click_effect.enable) return;

    const ripple = document.createElement('div');
    ripple.className = 'ripple gpu-accelerated';

    const size = Math.random() * 100 + 50;
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (e.clientX - size / 2) + 'px';
    ripple.style.top = (e.clientY - size / 2) + 'px';

    const color = document.documentElement.getAttribute('data-theme') === 'dark'
      ? butterfly_config.click_effect.dark
      : butterfly_config.click_effect.light;

    ripple.style.background = color;

    document.body.appendChild(ripple);

    setTimeout(() => {
      ripple.remove();
    }, 600);
  });
}

// 科技感鼠标跟随效果
function initTechCursorEffect() {
  const cursor = document.createElement('div');
  cursor.className = 'tech-cursor';
  cursor.style.cssText = `
    position: fixed;
    width: 20px;
    height: 20px;
    border: 2px solid rgba(79, 192, 245, 0.5);
    border-radius: 50%;
    pointer-events: none;
    z-index: 9999;
    transition: transform 0.1s ease;
    mix-blend-mode: difference;
  `;

  const cursorFollower = document.createElement('div');
  cursorFollower.className = 'tech-cursor-follower';
  cursorFollower.style.cssText = `
    position: fixed;
    width: 40px;
    height: 40px;
    background: rgba(79, 192, 245, 0.1);
    border-radius: 50%;
    pointer-events: none;
    z-index: 9998;
    transition: transform 0.3s ease;
  `;

  document.body.appendChild(cursor);
  document.body.appendChild(cursorFollower);

  let mouseX = 0, mouseY = 0;
  let cursorX = 0, cursorY = 0;
  let followerX = 0, followerY = 0;

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  function animateCursor() {
    cursorX += (mouseX - cursorX) * 0.5;
    cursorY += (mouseY - cursorY) * 0.5;

    followerX += (mouseX - followerX) * 0.1;
    followerY += (mouseY - followerY) * 0.1;

    cursor.style.left = cursorX - 10 + 'px';
    cursor.style.top = cursorY - 10 + 'px';

    cursorFollower.style.left = followerX - 20 + 'px';
    cursorFollower.style.top = followerY - 20 + 'px';

    requestAnimationFrame(animateCursor);
  }

  animateCursor();

  // 鼠标悬停在链接上时的效果
  const links = document.querySelectorAll('a, button, .card-widget');
  links.forEach(link => {
    link.addEventListener('mouseenter', () => {
      cursor.style.transform = 'scale(1.5)';
      cursor.style.borderColor = 'rgba(73, 177, 245, 0.8)';
      cursorFollower.style.transform = 'scale(1.2)';
    });

    link.addEventListener('mouseleave', () => {
      cursor.style.transform = 'scale(1)';
      cursor.style.borderColor = 'rgba(79, 192, 245, 0.5)';
      cursorFollower.style.transform = 'scale(1)';
    });
  });
}

// 粒子效果
function initParticles() {
  const config = butterfly_config.visual_effects.particles;

  // 如果已加载particles.js库，使用它
  if (typeof particlesJS !== 'undefined') {
    particlesJS('particles-js', {
      "particles": {
        "number": {
          "value": config.number,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": config.color
        },
        "shape": {
          "type": config.shape
        },
        "opacity": {
          "value": config.opacity,
          "random": false
        },
        "size": {
          "value": config.size,
          "random": true
        },
        "line_linked": {
          "enable": true,
          "distance": 150,
          "color": config.color,
          "opacity": 0.4,
          "width": 1
        },
        "move": {
          "enable": config.move.enable,
          "speed": config.move.speed,
          "direction": config.move.direction,
          "random": config.move.random,
          "straight": config.move.straight,
          "out_mode": config.move.out_mode,
          "bounce": config.move.bounce
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "repulse"
          },
          "onclick": {
            "enable": true,
            "mode": "push"
          }
        },
        "modes": {
          "repulse": {
            "distance": 100,
            "duration": 0.4
          },
          "push": {
            "particles_nb": 4
          }
        }
      },
      "retina_detect": true
    });
  } else {
    // 简单的粒子效果实现
    createSimpleParticles();
  }
}

// 简单的粒子效果实现
function createSimpleParticles() {
  const particlesContainer = document.createElement('div');
  particlesContainer.id = 'simple-particles';
  particlesContainer.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
  `;

  document.body.appendChild(particlesContainer);

  const config = butterfly_config.visual_effects.particles;

  for (let i = 0; i < config.number; i++) {
    createParticle(particlesContainer, config);
  }
}

function createParticle(container, config) {
  const particle = document.createElement('div');
  particle.style.cssText = `
    position: absolute;
    width: ${config.size}px;
    height: ${config.size}px;
    background: ${config.color};
    border-radius: ${config.shape === 'circle' ? '50%' : '0'};
    opacity: ${config.opacity};
    left: ${Math.random() * 100}%;
    top: ${Math.random() * 100}%;
    transition: transform ${config.move.speed}s linear;
    pointer-events: none;
  `;

  container.appendChild(particle);

  // 动画
  animateParticle(particle, config);
}

function animateParticle(particle, config) {
  const duration = config.move.speed * 1000;
  const startX = parseFloat(particle.style.left);
  const startY = parseFloat(particle.style.top);

  function move() {
    const angle = Math.random() * Math.PI * 2;
    const distance = 50 + Math.random() * 100;

    const newX = startX + Math.cos(angle) * distance;
    const newY = startY + Math.sin(angle) * distance;

    particle.style.transform = `translate(${newX - startX}px, ${newY - startY}px)`;

    setTimeout(() => {
      particle.style.transform = 'translate(0, 0)';
      setTimeout(move, duration);
    }, duration);
  }

  move();
}

// 星空效果
function initStarrySky() {
  const config = butterfly_config.visual_effects.starry_sky;
  const starryContainer = document.createElement('div');
  starryContainer.className = 'starry-sky';

  document.body.appendChild(starryContainer);

  for (let i = 0; i < config.star_count; i++) {
    createStar(starryContainer, config);
  }
}

function createStar(container, config) {
  const star = document.createElement('div');
  star.className = 'star';

  const size = Math.random() * 3;
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  const duration = 1 + Math.random() * 3;
  const delay = Math.random() * 3;

  star.style.cssText = `
    width: ${size}px;
    height: ${size}px;
    left: ${x}%;
    top: ${y}%;
    background: ${config.star_color};
    animation: twinkle ${duration}s ${delay}s infinite;
  `;

  container.appendChild(star);
}

// 打字机效果
function initTypewriter() {
  const config = butterfly_config.typewriter;
  const elements = document.querySelectorAll('.typewriter-text');

  elements.forEach(element => {
    typeWriter(element, config.text || element.textContent, config.typeSpeed, config.cursorChar);
  });
}

function typeWriter(element, text, speed, cursor) {
  let i = 0;
  element.textContent = '';

  function type() {
    if (i < text.length) {
      element.textContent += text.charAt(i);
      i++;
      setTimeout(type, speed);
    } else {
      if (!config.loop && cursor) {
        element.textContent += cursor;
        setInterval(() => {
          element.style.opacity = element.style.opacity === '0' ? '1' : '0';
        }, 500);
      }
    }
  }

  type();
}

// 动态渐变背景
function initAnimatedBackground() {
  if (document.querySelector('.animated-gradient')) return;

  const indexHeader = document.querySelector('#page-header');
  if (indexHeader) {
    indexHeader.classList.add('animated-gradient');
  }
}

// 霓虹文字效果
function initNeonGlow() {
  const config = butterfly_config.visual_effects.neon_glow;

  if (config.enable) {
    const titleElements = document.querySelectorAll('#page-title, .post-title, h1');
    titleElements.forEach(element => {
      element.classList.add('neon-text');
    });
  }
}

// 页面加载动画
window.addEventListener('load', function() {
  const loadingBox = document.getElementById('loading-box');
  if (loadingBox) {
    setTimeout(() => {
      loadingBox.style.opacity = '0';
      setTimeout(() => {
        loadingBox.remove();
      }, 500);
    }, 1000);
  }
});

// 主题切换时的背景调整
const observer = new MutationObserver(function(mutations) {
  mutations.forEach(function(mutation) {
    if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
      updateThemeBackground();
    }
  });
});

observer.observe(document.documentElement, {
  attributes: true,
  attributeFilter: ['data-theme']
});

function updateThemeBackground() {
  const theme = document.documentElement.getAttribute('data-theme');
  // 可以根据主题调整背景颜色或效果
  console.log('Theme changed to:', theme);
}