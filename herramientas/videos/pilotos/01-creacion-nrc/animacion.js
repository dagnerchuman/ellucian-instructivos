/**
 * ==============================================================================
 * HYPERFRAMES ANIMATION RUNTIME · UNIVERSIDAD SEÑOR DE SIPÁN (USS)
 * Composición: nrc-idiomas
 * Duración: 24 segundos (Render determinista cuadro a cuadro)
 * ==============================================================================
 */

(function() {
  // Crear el timeline maestro pausado requerido por HyperFrames
  const tl = gsap.timeline({ paused: true });

  // --- ESCENA 1: Carátula e Intro (0s - 6s) ---
  tl.fromTo("#clip-intro .intro-pill", 
    { opacity: 0, y: -25 }, 
    { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 
    0.2
  );

  tl.fromTo("#clip-intro .intro-title", 
    { opacity: 0, scale: 0.95, y: 30 }, 
    { opacity: 1, scale: 1, y: 0, duration: 1.0, ease: "power4.out" }, 
    0.5
  );

  tl.fromTo("#clip-intro .intro-desc", 
    { opacity: 0, y: 20 }, 
    { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 
    1.0
  );

  tl.fromTo("#clip-intro .mini-card", 
    { opacity: 0, y: 40 }, 
    { opacity: 1, y: 0, duration: 0.8, stagger: 0.18, ease: "back.out(1.4)" }, 
    1.4
  );

  // Transición suave de salida de la intro hacia la escena 2
  tl.to("#clip-intro .intro-container", 
    { opacity: 0, y: -40, duration: 0.6, ease: "power2.in" }, 
    5.4
  );

  // --- ESCENA 2: Programación en SSASECT (6s - 13s) ---
  tl.fromTo("#clip-ssasect .scene-header-step", 
    { opacity: 0, x: -50 }, 
    { opacity: 1, x: 0, duration: 0.8, ease: "power3.out" }, 
    6.1
  );

  tl.fromTo("#clip-ssasect .banner-window", 
    { opacity: 0, y: 60, scale: 0.97 }, 
    { opacity: 1, y: 0, scale: 1, duration: 0.9, ease: "power3.out" }, 
    6.4
  );

  // Entrada escalonada de los campos de SSASECT
  tl.fromTo("#clip-ssasect .form-field", 
    { opacity: 0, y: 25 }, 
    { opacity: 1, y: 0, duration: 0.5, stagger: 0.12, ease: "power2.out" }, 
    7.0
  );

  // Resaltado de la acción de guardado (F10)
  tl.fromTo("#clip-ssasect .banner-action-pill", 
    { opacity: 0, scale: 0.9 }, 
    { opacity: 1, scale: 1, duration: 0.7, ease: "back.out(1.6)" }, 
    9.2
  );

  // Transición de salida de SSASECT
  tl.to("#clip-ssasect .scene-container", 
    { opacity: 0, scale: 0.96, duration: 0.6, ease: "power2.in" }, 
    12.4
  );

  // --- ESCENA 3: Regla de Ligas TA y PA (13s - 19s) ---
  tl.fromTo("#clip-ligas .scene-header-step", 
    { opacity: 0, x: -50 }, 
    { opacity: 1, x: 0, duration: 0.8, ease: "power3.out" }, 
    13.1
  );

  // Entrada de las dos tarjetas de ligas (Teórica y Práctica)
  tl.fromTo("#clip-ligas .liga-card.teorica", 
    { opacity: 0, x: -60 }, 
    { opacity: 1, x: 0, duration: 0.9, ease: "power3.out" }, 
    13.5
  );

  tl.fromTo("#clip-ligas .liga-connector", 
    { opacity: 0, scale: 0.5 }, 
    { opacity: 1, scale: 1, duration: 0.8, ease: "elastic.out(1, 0.6)" }, 
    14.0
  );

  tl.fromTo("#clip-ligas .liga-card.practica", 
    { opacity: 0, x: 60 }, 
    { opacity: 1, x: 0, duration: 0.9, ease: "power3.out" }, 
    14.4
  );

  // Transición de salida de Ligas
  tl.to("#clip-ligas .scene-container", 
    { opacity: 0, y: -40, duration: 0.6, ease: "power2.in" }, 
    18.4
  );

  // --- ESCENA 4: Cierre y Auditoría en SSASECQ (19s - 24s) ---
  tl.fromTo("#clip-cierre .success-icon", 
    { opacity: 0, scale: 0.3, rotation: -30 }, 
    { opacity: 1, scale: 1, rotation: 0, duration: 0.9, ease: "back.out(1.8)" }, 
    19.1
  );

  tl.fromTo("#clip-cierre .outro-title", 
    { opacity: 0, y: 30 }, 
    { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }, 
    19.5
  );

  tl.fromTo("#clip-cierre .outro-desc", 
    { opacity: 0, y: 20 }, 
    { opacity: 1, y: 0, duration: 0.7, ease: "power2.out" }, 
    19.9
  );

  tl.fromTo("#clip-cierre .meta-item", 
    { opacity: 0, y: 30 }, 
    { opacity: 1, y: 0, duration: 0.6, stagger: 0.15, ease: "power2.out" }, 
    20.3
  );

  tl.fromTo("#clip-cierre .video-footer", 
    { opacity: 0 }, 
    { opacity: 1, duration: 0.9, ease: "power1.out" }, 
    21.2
  );

  // Registrar el timeline en el objeto global requerido por el motor HyperFrames
  window.__timelines = window.__timelines || {};
  window.__timelines["nrc-idiomas"] = tl;
})();
