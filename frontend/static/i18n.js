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
    yes: "Yes"
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
    yes: "Ja"
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
    yes: "Oui"
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
    yes: "Sí"
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

// Apply translations when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  applyUITranslations();
});
