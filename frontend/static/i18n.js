/* ==========================================================================
   UI LANGUAGE DICT
   ========================================================================== */
// static/i18n.js

const UI_TRANSLATIONS = {
  en: {
  loadPosts: "Load Posts",
  login: "Login",
  logout: "Logout",
  signup: "Sign up",
  addPost: "Add Post",
  welcome: "Welcome",
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
  allCategories: "All Categories"
},
  de: {
  loadPosts: "Beiträge laden",
  login: "Anmelden",
  logout: "Abmelden",
  signup: "Registrieren",
  addPost: "Beitrag hinzufügen",
  welcome: "Willkommen",
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
  allCategories: "Alle Kategorien"
},
  fr: {
  loadPosts: "Charger les articles",
  login: "Connexion",
  logout: "Déconnexion",
  signup: "S'inscrire",
  addPost: "Ajouter un article",
  welcome: "Bienvenue",
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
  allCategories: "Toutes les catégories"
},
  es: {
  loadPosts: "Cargar publicaciones",
  login: "Iniciar sesión",
  logout: "Cerrar sesión",
  signup: "Registrarse",
  addPost: "Agregar publicación",
  welcome: "Bienvenido",
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
  allCategories: "Todas las categorías"
}
}
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

  // Option text translations (🛠 now inside the function!)
  document.querySelectorAll("select[data-i18n-option]").forEach(select => {
    select.querySelectorAll("option").forEach(option => {
      const key = option.getAttribute("data-i18n-option");
      if (key && strings[key]) {
        option.textContent = strings[key];
      }
    });
  });

  // Translate default category filter (first <option>)
  const catSel = document.getElementById("filter-category");
  if (catSel && catSel.options.length > 0) {
    const firstOption = catSel.options[0];
    if (firstOption.value === "") {
      firstOption.textContent = strings.allCategories || "All Categories";
    }
  }

  // Update welcome message
  const username = localStorage.getItem("username");
  if (username && strings.welcome) {
    document.getElementById("user-info").textContent = `${strings.welcome}, ${username}!`;
  } else {
    document.getElementById("user-info").textContent = "";
  }
}
