/* ==========================================================================
   UI LANGUAGE DICTIONARY & TRANSLATION LOGIC
   ========================================================================== */
const UI_TRANSLATIONS = {
  en: {
    loadPosts: "Load Posts",
    login: "Login",
    logout: "Logout",
    signup: "Sign up",
    addPost: "Add Post",
    welcome: "Welcome",
    editPost: "Edit",
    deletePost: "Delete",
    comments: "Comments",
    commentPlaceholder: "Add a comment...",
    postComment: "Post Comment",
    searchPlaceholder: "Search posts...",
    applyFilters: "Apply Filters",
    noSorting: "No Sorting",
    sortAuthor: "Author",
    sortTitle: "Title",
    sortLikes: "Likes",
    sortDate: "Date",
    sortUpdated: "Last Updated",
    ascending: "Ascending",
    descending: "Descending",
    allCategories: "All Categories",
    updatedLabel: "Updated:",
    by: "by",
    aiTranslated: "AI-translated",
    title: "Title",
    content: "Content",
    category: "Category",
    save: "Save",
    saved: "Saved",
    invalid: "Invalid",
    emailExample: "you@example.com",
    cancel: "Cancel",
    update: "Update",
    titlePlaceholder: "Title",
    contentPlaceholder: "Content",
    usernamePlaceholder: "Username",
    passwordPlaceholder: "Password",
    selectCategory: "Select Category",
    loginRequired: "Login Required",
    loginToAdd: "You need to be logged in to add a post.",
    mustBeLoggedIn: "You must be logged in to add a post.",
    yes: "Yes",
    readAloud: "Read Aloud (Demo)",
    ttsUsedUp: "⚠️ You've used your demo listen. Upgrade required for more.",
    "getnotif": "Get notified on likes & comments",   // when no email is stored
    "noEmailSet": "Please save email first",    // when clicked on getnotif but no email is stored
    "invalid": "Invalid", // when user enters false email format
    "notificationsOn": "Notifications ON", // only shows when email is stored and notifications_enabled = 1
    "notificationsOff": "Notifications disabled — click to enable", // only shows when email is stored and notifications_enabled = 0
    "infoTitle": "Welcome to The Quiet Almanac",
"infoIntro": "Originally a school assignment, this project was expanded to explore core concepts in full-stack development. It brings together multilingual publishing, AI integrations, and a focus on user experience.",
"infoFeaturesTitle": "Highlights:",
"infoFeature1": "✅ Multilingual interface with AI-generated post translations (EN, DE, FR, ES)",
"infoFeature2": "✅ AI moderation system filters out harmful or unsafe content",
"infoFeature3": "✅ One-time demo of AI text-to-speech (TTS) for post narration",
"infoFeature4": "✅ Smart limitations to prevent spam and abuse (rate, length, repetition)",
"infoFeature5": "✅ Injection-safe form handling with sanitized inputs",
"infoFeature6": "✅ Email notifications toggle for post likes & comments",
"infoFeature7": "✅ Token-based login system with protected endpoints",
"infoFeature8": "✅ Translation caching for fast, on-demand reuse",
"infoFeature9": "✅ Secure post/comment management with live updates",
"infoFeature10": "⚠️ Category, comment, and date translation ",
"infoClose": "Explore the App",
disclaimerNoticePrefix: "This is a study project.",
    disclaimerLink: "Read full disclaimer",
    githubLinePrefix: "View source & README on",
    githubLink: "GitHub",
    disclaimerTitle: "⚠️ Disclaimer",
    disclaimerItems: [
      "This is a study project created as part of a backend & AI engineering curriculum.",
      "No guarantees are provided regarding performance, security, or data persistence.",
      "AI-generated translations, moderation, and TTS may contain inaccuracies or unpredictable behavior.",
      "Email notifications are sent only to demo/test addresses and are not production-secure.",
      'The “Upgrade Required” TTS message is a demo placeholder — no upsell or payment exists.',
      "Use at your own risk. The developer assumes no liability for any outcomes resulting from usage."
    ],
    disclaimerClose: "Close"

  },
  de: {
    loadPosts: "Beiträge laden",
    login: "Anmelden",
    logout: "Abmelden",
    signup: "Registrieren",
    addPost: "Beitrag hinzufügen",
    welcome: "Willkommen",
    editPost: "Bearbeiten",
    deletePost: "Löschen",
    comments: "Kommentare",
    commentPlaceholder: "Kommentar hinzufügen...",
    postComment: "Kommentar posten",
    searchPlaceholder: "Beiträge durchsuchen...",
    applyFilters: "Filter anwenden",
    noSorting: "Keine Sortierung",
    sortAuthor: "Autor",
    sortTitle: "Titel",
    sortLikes: "Gefällt mir",
    sortDate: "Datum",
    sortUpdated: "Zuletzt aktualisiert",
    ascending: "Aufsteigend",
    descending: "Absteigend",
    allCategories: "Alle Kategorien",
    updatedLabel: "Aktualisiert:",
    by: "von",
    aiTranslated: "KI-übersetzt",
    title: "Titel",
    content: "Inhalt",
    category: "Kategorie",
    save: "Speichern",
    saved: "Gespeichert",
    emailExample: "du@beispiel.de",
    cancel: "Abbrechen",
    update: "Aktualisieren",
    titlePlaceholder: "Titel",
    contentPlaceholder: "Inhalt",
    usernamePlaceholder: "Benutzername",
    passwordPlaceholder: "Passwort",
    selectCategory: "Kategorie auswählen",
    loginRequired: "Anmeldung erforderlich",
    loginToAdd: "Du musst angemeldet sein, um einen Beitrag hinzuzufügen.",
    mustBeLoggedIn: "Du musst angemeldet sein, um einen Beitrag zu erstellen.",
    yes: "Ja",
    readAloud: "Vorlesen (Demo)",
    ttsUsedUp: "⚠️ Du hast dein Demovorlesen verwendet. Upgrade erforderlich für mehr.",
    "getnotif": "Lass dich über Likes & Kommentare benachrichtigen",
    "noEmailSet": "Bitte zuerst E-Mail speichern",
    "invalid": "Ungültig",
    "notificationsOn": "Benachrichtigungen AKTIV",
    "notificationsOff": "Benachrichtigungen deaktiviert — zum Aktivieren klicken",
      "infoTitle": "Willkommen bei The Quiet Almanac",
  "infoIntro": "Ursprünglich als Schulprojekt gestartet, wurde diese App erweitert, um zentrale Konzepte der Full-Stack-Entwicklung zu vertiefen. Sie kombiniert mehrsprachiges Publishing, KI-gestützte Funktionen und ein benutzerfreundliches UX-Design.",
  "infoFeaturesTitle": "Highlights:",
  "infoFeature1": "✅ Mehrsprachige Oberfläche mit KI-gestützter Übersetzung von Posts (EN, DE, FR, ES)",
  "infoFeature2": "✅ KI-Moderation erkennt und filtert unangemessene oder sensible Inhalte",
  "infoFeature3": "✅ Einmalige Demo: KI-gestützte Sprachausgabe (TTS) für Posts",
  "infoFeature4": "✅ Intelligente Begrenzungen gegen Spam und Missbrauch (Frequenz, Länge, Wiederholungen)",
  "infoFeature5": "✅ Sichere Formularverarbeitung durch automatische Eingabe-Säuberung",
  "infoFeature6": "✅ E-Mail-Benachrichtigungen bei Likes und Kommentaren (deaktivierbar)",
  "infoFeature7": "✅ Token-basierter Login mit geschützten Schnittstellen",
  "infoFeature8": "✅ Übersetzungs-Cache für schnelle, wiederverwendbare Ergebnisse",
  "infoFeature9": "✅ Sichere Post- und Kommentar-Verwaltung mit Live-Aktualisierung",
  "infoFeature10": "⚠️ Kategorien, Kommentare und Datumsangaben sind derzeit nicht übersetzt",
  "infoClose": "App erkunden",
  disclaimerNoticePrefix: "Dies ist ein Studienprojekt.",
    disclaimerLink: "Vollständigen Haftungsausschluss lesen",
    githubLinePrefix: "Quellcode & README auf",
    githubLink: "GitHub",
    disclaimerTitle: "⚠️ Haftungsausschluss",
    disclaimerItems: [
      "Dies ist ein Studienprojekt im Rahmen eines Backend- & KI-Engineering-Kurses.",
      "Es wird keine Garantie für Leistung, Sicherheit oder Datenpersistenz übernommen.",
      "KI-gestützte Übersetzungen, Moderation und Sprachausgabe können Ungenauigkeiten oder unvorhersehbares Verhalten enthalten.",
      "E-Mail-Benachrichtigungen werden nur zu Demo-/Testzwecken gesendet und sind nicht für die Produktion gedacht.",
      "Die Meldung „Upgrade erforderlich“ bei der Sprachausgabe ist ein Demo-Platzhalter – es gibt kein Upsell oder Zahlungssystem.",
      "Nutzung auf eigene Gefahr. Der Entwickler übernimmt keine Haftung für Folgen aus der Nutzung."
    ],
    disclaimerClose: "Schließen"
  },
  fr: {
    loadPosts: "Charger les articles",
    login: "Connexion",
    logout: "Déconnexion",
    signup: "S'inscrire",
    addPost: "Ajouter un article",
    welcome: "Bienvenue",
    editPost: "Modifier",
    deletePost: "Supprimer",
    comments: "Commentaires",
    commentPlaceholder: "Ajouter un commentaire...",
    postComment: "Publier un commentaire",
    searchPlaceholder: "Rechercher des articles...",
    applyFilters: "Appliquer les filtres",
    noSorting: "Aucun tri",
    sortAuthor: "Auteur",
    sortTitle: "Titre",
    sortLikes: "Mentions J’aime",
    sortDate: "Date",
    sortUpdated: "Dernière modification",
    ascending: "Ascendant",
    descending: "Descendant",
    allCategories: "Toutes les catégories",
    updatedLabel: "Mis à jour :",
    by: "par",
    aiTranslated: "Traduit par IA",
    title: "Titre",
    content: "Contenu",
    category: "Catégorie",
    save: "Enregistrer",
    saved: "Enregistré",
    emailExample: "vous@exemple.fr",
    cancel: "Annuler",
    update: "Mettre à jour",
    titlePlaceholder: "Titre",
    contentPlaceholder: "Contenu",
    usernamePlaceholder: "Nom d'utilisateur",
    passwordPlaceholder: "Mot de passe",
    selectCategory: "Sélectionner une catégorie",
    loginRequired: "Connexion requise",
    loginToAdd: "Vous devez être connecté pour ajouter un article.",
    mustBeLoggedIn: "Vous devez être connecté pour publier un article.",
    yes: "Oui",
    readAloud: "Lecture à voix haute (Démo)",
    ttsUsedUp: "⚠️ Vous avez utilisé votre écoute démo. Mise à niveau requise pour plus.",
    "getnotif": "Recevez des notifications pour les likes et les commentaires",
    "noEmailSet": "Veuillez d'abord enregistrer une adresse e-mail",
    "invalid": "Invalide",
    "notificationsOn": "Notifications ACTIVÉES",
    "notificationsOff": "Notifications désactivées — cliquez pour activer",
    "infoTitle": "Bienvenue sur The Quiet Almanac",
  "infoIntro": "Initialement un projet scolaire, cette application a été développée pour approfondir les concepts clés du développement full-stack. Elle réunit la publication multilingue, des intégrations d’IA, et une expérience utilisateur soignée.",
  "infoFeaturesTitle": "Fonctionnalités principales :",
  "infoFeature1": "✅ Interface multilingue avec traduction automatique des posts par IA (EN, DE, FR, ES)",
  "infoFeature2": "✅ Système de modération IA pour filtrer les contenus sensibles ou inappropriés",
  "infoFeature3": "✅ Démonstration unique de synthèse vocale (TTS) par IA pour lire les posts",
  "infoFeature4": "✅ Limitations intelligentes pour prévenir le spam et les abus (fréquence, longueur, répétition)",
  "infoFeature5": "✅ Traitement sécurisé des formulaires avec nettoyage automatique des données",
  "infoFeature6": "✅ Notifications par e-mail pour les likes et commentaires (option désactivable)",
  "infoFeature7": "✅ Connexion via token avec protection des points d'accès",
  "infoFeature8": "✅ Mise en cache des traductions pour des performances accrues",
  "infoFeature9": "✅ Gestion sécurisée des posts et commentaires avec mises à jour en direct",
  "infoFeature10": "⚠️ Les catégories, commentaires et dates ne sont pas encore traduits",
  "infoClose": "Explorer l’application",
  disclaimerNoticePrefix: "Ceci est un projet d'étude.",
    disclaimerLink: "Lire l'avertissement complet",
    githubLinePrefix: "Voir le code source et le README sur",
    githubLink: "GitHub",
    disclaimerTitle: "⚠️ Avertissement",
    disclaimerItems: [
      "Ceci est un projet d’étude réalisé dans le cadre d’un cursus en backend et ingénierie de l’IA.",
      "Aucune garantie n’est fournie concernant les performances, la sécurité ou la conservation des données.",
      "Les traductions, modérations et synthèses vocales générées par l’IA peuvent comporter des erreurs ou un comportement imprévisible.",
      "Les notifications par e-mail sont envoyées uniquement à des adresses de test/démonstration et ne sont pas sécurisées pour un usage en production.",
      "Le message vocal « Mise à niveau requise » est un simple exemple – il n’y a ni vente ni paiement.",
      "Utilisez à vos propres risques. Le développeur décline toute responsabilité en cas de problème."
    ],
    disclaimerClose: "Fermer"
    },
  es: {
    loadPosts: "Cargar publicaciones",
    login: "Iniciar sesión",
    logout: "Cerrar sesión",
    signup: "Registrarse",
    addPost: "Agregar publicación",
    welcome: "Bienvenido",
    editPost: "Editar",
    deletePost: "Eliminar",
    comments: "Comentarios",
    commentPlaceholder: "Agregar un comentario...",
    postComment: "Publicar comentario",
    searchPlaceholder: "Buscar publicaciones...",
    applyFilters: "Aplicar filtros",
    noSorting: "Sin orden",
    sortAuthor: "Autor",
    sortTitle: "Título",
    sortLikes: "Me gusta",
    sortDate: "Fecha",
    sortUpdated: "Última actualización",
    ascending: "Ascendente",
    descending: "Descendente",
    allCategories: "Todas las categorías",
    updatedLabel: "Actualizado:",
    by: "por",
    aiTranslated: "Traducido por IA",
    title: "Título",
    content: "Contenido",
    category: "Categoría",
    save: "Guardar",
    saved: "Guardado",
    emailExample: "tú@ejemplo.es",
    cancel: "Cancelar",
    update: "Actualizar",
    titlePlaceholder: "Título",
    contentPlaceholder: "Contenido",
    usernamePlaceholder: "Nombre de usuario",
    passwordPlaceholder: "Contraseña",
    selectCategory: "Seleccionar categoría",
    loginRequired: "Se requiere inicio de sesión",
    loginToAdd: "Debes iniciar sesión para agregar una publicación.",
    mustBeLoggedIn: "Debes iniciar sesión para publicar una entrada.",
    yes: "Sí",
    readAloud: "Leer en voz alta (Demostración)",
    ttsUsedUp: "⚠️ Has usado tu demostración. Se requiere mejora para más.",
    "getnotif": "Recibe notificaciones sobre me gusta y comentarios",
    "noEmailSet": "Por favor guarda tu correo electrónico primero",
    "invalid": "Inválido",
    "notificationsOn": "Notificaciones ACTIVADAS",
    "notificationsOff": "Notificaciones desactivadas — haz clic para activar",
    "infoTitle": "Bienvenido a The Quiet Almanac",
  "infoIntro": "Este proyecto comenzó como una tarea escolar y fue ampliado para profundizar en conceptos clave del desarrollo full-stack. Combina publicación multilingüe, funciones con IA y una experiencia de usuario bien pensada.",
  "infoFeaturesTitle": "Funciones destacadas:",
  "infoFeature1": "✅ Interfaz multilingüe con traducciones automáticas de publicaciones mediante IA (EN, DE, FR, ES)",
  "infoFeature2": "✅ Moderación con IA para filtrar contenido sensible o inapropiado",
  "infoFeature3": "✅ Demostración única de texto a voz (TTS) con IA para narrar publicaciones",
  "infoFeature4": "✅ Limitaciones inteligentes para evitar spam y abuso (frecuencia, longitud, repetición)",
  "infoFeature5": "✅ Procesamiento seguro de formularios con saneamiento de entradas",
  "infoFeature6": "✅ Notificaciones por correo electrónico sobre likes y comentarios (se puede desactivar)",
  "infoFeature7": "✅ Inicio de sesión con token y rutas protegidas",
  "infoFeature8": "✅ Caché de traducciones para reutilización rápida",
  "infoFeature9": "✅ Gestión segura de publicaciones y comentarios con actualizaciones en tiempo real",
  "infoFeature10": "⚠️ Categorías, comentarios y fechas aún no están traducidos",
  "infoClose": "Explorar la app",
  disclaimerNoticePrefix: "Este es un proyecto de estudio.",
    disclaimerLink: "Leer la declaración completa",
    githubLinePrefix: "Ver el código fuente y el README en",
    githubLink: "GitHub",
    disclaimerTitle: "⚠️ Aviso legal",
    disclaimerItems: [
      "Este es un proyecto de estudio creado como parte de un curso de backend e ingeniería de IA.",
      "No se ofrecen garantías sobre el rendimiento, la seguridad o la persistencia de datos.",
      "Las traducciones, moderaciones y lecturas generadas por IA pueden contener errores o comportamientos impredecibles.",
      "Las notificaciones por correo electrónico se envían solo a direcciones de prueba/demostración y no son seguras para producción.",
      'El mensaje de TTS “Se requiere actualización” es un marcador de demostración — no existe venta ni pago.',
      "Úselo bajo su propia responsabilidad. El desarrollador no se hace responsable de los resultados derivados del uso."
    ],
    disclaimerClose: "Cerrar"
  }
};

function getCurrentLanguage() {
  return localStorage.getItem("lang") || "en";
}

function applyUITranslations() {
  const lang = getCurrentLanguage();
  const strings = UI_TRANSLATIONS[lang];

  // Text content replacements
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (strings[key]) el.textContent = strings[key];
  });

  // Placeholder replacements
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (strings[key]) el.placeholder = strings[key];
  });

  // Option text replacements
  document.querySelectorAll("select[data-i18n-option]").forEach(select => {
    select.querySelectorAll("option").forEach(option => {
      const key = option.getAttribute("data-i18n-option");
      if (key && strings[key]) {
        option.textContent = strings[key];
      }
    });
  });

  // Update default "All Categories" option
  const catSel = document.getElementById("filter-category");
  if (catSel && catSel.options.length > 0) {
    const firstOption = catSel.options[0];
    if (firstOption.value === "") {
      firstOption.textContent = strings.allCategories || "All Categories";
    }
  }

  // Welcome message
  const username = localStorage.getItem("username");
  if (username && strings.welcome) {
    document.getElementById("user-info").textContent = `${strings.welcome}, ${username}!`;
  } else {
    document.getElementById("user-info").textContent = "";
  }
}

function translate(key) {
  const lang = getCurrentLanguage();
  const strings = UI_TRANSLATIONS[lang] || {};
  return strings[key] || key;
}
// Apply translations when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  applyUITranslations();
});
