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
    "getnotif": "Get notified on likes & comments",   // when no email stored
    "noEmailSet": "Please save email first",    // when user tries toggle without email
    "invalid": "Invalid",
    "notificationsOn": "Notifications ON",
    "notificationsOff": "Notifications disabled — click to enable",
    infoTitle: "Welcome,",
    infoIntro: "This is a portfolio project showcasing multilingual, AI-assisted blog translation, AI moderation, text-to-speech, and more.",
    infoFeaturesTitle: "What this app can do:",
    infoFeature1: "✅ Multilingual UI and AI-powered post translations (EN, DE, FR, ES)",
    infoFeature2: "✅ Dynamic translation caching for performance",
    infoFeature3: "✅ Create, edit, and delete posts with authentication",
    infoFeature4: "✅ Token-based login/logout and user session control",
    infoFeature5: "✅ Email notifications when your post gets liked or commented",
    infoFeature6: "✅ Comments system with live updates",
    infoFeature7: "✅ AI moderation to detect harmful content",
    infoFeature8: "✅ Prevents abuse with title/content length checks and post repetition limits",
    infoFeature9: "✅ Text-to-speech (TTS) demo for reading posts aloud (one-time usage)",
    infoFeature10: "⚠️ Categories, comments, and date are not yet translated",
    infoClose: "Got it!"
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
    "noEmailSet": "Bitte gib zuerst deine E-Mail-Adresse ein",
    "notificationsOn": "Benachrichtigungen AKTIV",
    "notificationsOff": "Benachrichtigungen deaktiviert – zum Aktivieren klicken",
    infoTitle: "Willkommen,",
    infoIntro: "Dies ist ein Portfolio-Projekt, das mehrsprachige, KI-gestützte Blog-Übersetzung, KI-Moderation, Text-to-Speech und mehr demonstriert.",
    infoFeaturesTitle: "Was diese App kann:",
    infoFeature1: "✅ Mehrsprachige Oberfläche und KI-gestützte Beitragsübersetzung (EN, DE, FR, ES)",
    infoFeature2: "✅ Dynamisches Caching von Übersetzungen für bessere Leistung",
    infoFeature3: "✅ Beiträge erstellen, bearbeiten und löschen mit Authentifizierung",
    infoFeature4: "✅ Token-basierte Anmeldung/Abmeldung und Sitzungsverwaltung",
    infoFeature5: "✅ E-Mail-Benachrichtigungen bei Likes oder Kommentaren",
    infoFeature6: "✅ Kommentarsystem mit Live-Aktualisierung",
    infoFeature7: "✅ KI-Moderation erkennt schädliche Inhalte",
    infoFeature8: "✅ Missbrauchsschutz durch Längen- und Wiederholungsbeschränkung bei Beiträgen",
    infoFeature9: "✅ Text-to-Speech (TTS) Demo zum Vorlesen (einmalige Nutzung)",
    infoFeature10: "⚠️ Kategorien, Kommentare und Datum werden noch nicht übersetzt",
    infoClose: "Verstanden!"
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
    "noEmailSet": "Veuillez d’abord entrer votre adresse e-mail",
    "notificationsOn": "Notifications ACTIVÉES",
    "notificationsOff": "Notifications désactivées — cliquez pour activer",
    infoTitle: "Bienvenue,",
    infoIntro: "Il s'agit d'un projet portfolio mettant en avant la traduction de blogs multilingue assistée par IA, la modération par IA, la synthèse vocale, et plus encore.",
    infoFeaturesTitle: "Ce que cette application peut faire :",
    infoFeature1: "✅ Interface multilingue et traduction automatique des articles (EN, DE, FR, ES)",
    infoFeature2: "✅ Mise en cache dynamique des traductions pour de meilleures performances",
    infoFeature3: "✅ Créer, modifier et supprimer des articles avec authentification",
    infoFeature4: "✅ Connexion/déconnexion basée sur des jetons et gestion de session",
    infoFeature5: "✅ Notifications par e-mail lors d’un like ou commentaire",
    infoFeature6: "✅ Système de commentaires avec mise à jour en temps réel",
    infoFeature7: "✅ Modération IA pour détecter le contenu nocif",
    infoFeature8: "✅ Protection contre les abus via des limites de longueur et de fréquence",
    infoFeature9: "✅ Démo Text-to-Speech (TTS) pour lire les articles à voix haute (une seule fois)",
    infoFeature10: "⚠️ Les catégories, les commentaires et la date ne sont pas encore traduits",
    infoClose: "Compris !"
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
    "noEmailSet": "Por favor, introduce tu correo electrónico primero",
    "notificationsOn": "Notificaciones ACTIVADAS",
    "notificationsOff": "Notificaciones desactivadas — haz clic para activar",
    infoTitle: "Bienvenido,",
    infoIntro: "Este es un proyecto de portafolio que presenta la traducción de blogs multilingüe asistida por IA, la moderación por IA, la conversión de texto a voz y mucho más.",
    infoFeaturesTitle: "Lo que puede hacer esta aplicación:",
    infoFeature1: "✅ Interfaz multilingüe y traducción automática de publicaciones (EN, DE, FR, ES)",
    infoFeature2: "✅ Caché dinámico de traducciones para mejorar el rendimiento",
    infoFeature3: "✅ Crear, editar y eliminar publicaciones con autenticación",
    infoFeature4: "✅ Inicio/cierre de sesión con tokens y control de sesión",
    infoFeature5: "✅ Notificaciones por correo electrónico cuando alguien da like o comenta",
    infoFeature6: "✅ Sistema de comentarios con actualizaciones en tiempo real",
    infoFeature7: "✅ Moderación IA para detectar contenido dañino",
    infoFeature8: "✅ Prevención de abuso mediante restricciones de longitud y repetición",
    infoFeature9: "✅ Demostración de texto a voz (TTS) para leer en voz alta (una sola vez)",
    infoFeature10: "⚠️ Las categorías, los comentarios y la fecha aún no están traducidos",
    infoClose: "¡Entendido!"
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
