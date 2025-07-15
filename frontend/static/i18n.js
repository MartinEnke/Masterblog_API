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
    loginToComment: "Login first to comment",
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
    emailDeleted: "Email deleted.",
    invalid: "Invalid",
    emailExample: "you@example.com",
    signupOrLoginFirst: "Signup or Login first.",
    passwordTooWeak: "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.",
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
    "getnotif": "Get notified on likes & comments",
    "noEmailSet": "Please save email first",
    "invalid": "Invalid",
    "notificationsOn": "Notifications ON",
    "notificationsOff": "Notifications disabled — click to enable",
    "infoTitle": "Welcome!",
"infoIntro": "This project began as a school assignment and grew into an exploration of core backend and frontend web development, featuring multilingual publishing and AI-powered tools.",
"infoFeaturesTitle": "Highlights:",
"infoFeature1": "✅ Multilingual fullstack blog with AI-powered post translations (EN, DE, FR, ES) and translation caching for fast response",
"infoFeature2": "✅ AI moderation ensures safe and respectful user interactions",
"infoFeature3": "✅ AI text-to-speech (TTS) for post narration (demo with limited access)",
"infoFeature4": "✅ Secure authentication: token-based login, scrypt password hashing, injection-safe inputs",
"infoFeature5": "✅ Responsive UI built with vanilla JS/Tailwind, fully translated frontend experience",
"infoFeature6": "✅ Swagger-documented REST API for clean, maintainable backend",
"infoFeature7": "✅ User engagement features including email notifications and spam protection",
"infoClose": "Explore the App",
disclaimerNoticePrefix: "This is a study project.",
    disclaimerLink: "Read full disclaimer",
    githubLinePrefix: "View source & README on",
    githubLink: "GitHub",
    disclaimerTitle: "⚠️ Disclaimer",
    disclaimerItems: [
      "This is a study project created as part of a backend & AI engineering curriculum.",
      "No guarantees are provided regarding performance, security, or data persistence.",
      "AI-generated translations, moderation, and TTS may contain inaccuracies.",
      "Emails are stored securely, used only for notifications, and can be fully deleted at any time.",
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
    loginToComment: "Anmeldung erforderlich.",
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
    signupOrLoginFirst: "Bitte zuerst registrieren oder anmelden.",
    passwordTooWeak: "Das Passwort muss mindestens 8 Zeichen lang sein und Großbuchstaben, Kleinbuchstaben, Zahlen und Sonderzeichen enthalten.",
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
      "infoTitle": "Willkommen!",
  "infoIntro": "Ursprünglich als Schulprojekt gestartet, wurde diese App erweitert, um zentrale Konzepte der Backend- und Frontend-Entwicklung zu vertiefen, inklusive mehrsprachigem Publishing und KI-gestützten Funktionen.",
  "infoFeaturesTitle": "Highlights:",
"infoFeature1": "✅ Mehrsprachiges Fullstack-Blog mit KI-gestützten Beitragsübersetzungen (EN, DE, FR, ES) und schneller Zwischenspeicherung",
"infoFeature2": "✅ KI-Moderation sorgt für sichere und respektvolle Nutzerinteraktionen",
"infoFeature3": "✅ KI-Text-zu-Sprache (TTS) für Beitragsvorlesungen (Demo mit eingeschränktem Zugang)",
"infoFeature4": "✅ Sichere Anmeldung mit Token, scrypt-Passworthashing und Schutz vor Eingabe-Injektionen",
"infoFeature5": "✅ Responsives Frontend mit Vanilla JS und Tailwind, komplett übersetzt",
"infoFeature6": "✅ REST-API mit Swagger dokumentiert für sauberen und wartungsfreundlichen Code",
"infoFeature7": "✅ Funktionen zur Nutzerbindung wie E-Mail-Benachrichtigungen und Spam-Schutz",
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
      "E-Mails werden sicher gespeichert, nur für Benachrichtigungen verwendet und können jederzeit vollständig gelöscht werden.",
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
    loginToComment: "Connectez-vous d'abord pour commenter",
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
    signupOrLoginFirst: "Veuillez d'abord vous inscrire ou vous connecter.",
    passwordTooWeak: "Le mot de passe doit contenir au moins 8 caractères, avec des majuscules, minuscules, chiffres et caractères spéciaux.",
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
    "infoTitle": "Bienvenue!",
  "infoIntro": "Ce projet a commencé comme un devoir scolaire et s'est transformé en une exploration des concepts fondamentaux du développement backend et frontend, avec une publication multilingue et des outils alimentés par l'IA.",
"infoFeaturesTitle": "Points forts :",
"infoFeature1": "✅ Blog fullstack multilingue avec traductions automatiques des articles (EN, DE, FR, ES) et mise en cache pour des réponses rapides",
"infoFeature2": "✅ La modération par IA garantit des interactions utilisateur sûres et respectueuses",
"infoFeature3": "✅ Synthèse vocale IA (TTS) pour la narration des articles (démo avec accès limité)",
"infoFeature4": "✅ Authentification sécurisée : connexion par token, hachage de mot de passe scrypt, entrées sécurisées contre les injections",
"infoFeature5": "✅ Interface responsive construite avec vanilla JS/Tailwind, expérience frontend entièrement traduite",
"infoFeature6": "✅ API REST documentée avec Swagger pour un backend propre et maintenable",
"infoFeature7": "✅ Fonctionnalités d'engagement utilisateur incluant notifications par e-mail et protection anti-spam",
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
      "Les e-mails sont stockés en toute sécurité, utilisés uniquement pour les notifications et peuvent être entièrement supprimés à tout moment.",
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
    loginToComment: "Inicia sesión para comentar",
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
    signupOrLoginFirst: "Regístrate o inicia sesión primero.",
    passwordTooWeak: "La contraseña debe tener al menos 8 caracteres e incluir mayúsculas, minúsculas, números y caracteres especiales.",
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
    "infoTitle": "Bienvenido!",
  "infoIntro": "Este proyecto comenzó como una tarea escolar y se convirtió en una exploración del desarrollo web backend y frontend, con publicación multilingüe y herramientas impulsadas por IA.",
"infoFeaturesTitle": "Aspectos destacados:",
"infoFeature1": "✅ Blog fullstack multilingüe con traducciones automáticas de publicaciones (EN, DE, FR, ES) y caché de traducción para respuesta rápida",
"infoFeature2": "✅ La moderación por IA garantiza interacciones seguras y respetuosas entre usuarios",
"infoFeature3": "✅ Texto a voz (TTS) por IA para narración de publicaciones (demo con acceso limitado)",
"infoFeature4": "✅ Autenticación segura: inicio de sesión con token, hash de contraseña scrypt, entradas seguras contra inyecciones",
"infoFeature5": "✅ UI responsiva construida con vanilla JS/Tailwind, experiencia frontend totalmente traducida",
"infoFeature6": "✅ API REST documentada con Swagger para un backend limpio y mantenible",
"infoFeature7": "✅ Funciones de interacción del usuario incluyendo notificaciones por correo electrónico y protección contra spam",
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
      "Los correos electrónicos se almacenan de forma segura, se utilizan solo para notificaciones y se pueden eliminar completamente en cualquier momento.",
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
