This package implements the SPPAS spin-off TextCueS web application following a
Model–View–Controller (MVC) architecture with a clear separation of concerns.

- **TextCueSLauncherRecipe** and **TextCueSResponseRecipe** act as the 
  *HTTP transport layer*. They handle request/response flow, HTTP status management, 
  and page delivery to the client. They remain focused on communication and 
  response serialization.

- **TextCueSController** represents the *MVC controller*.
  It manages the application logic: interacting with the model, and invoking the
  view to construct the HTML representation of the content.

- **TextCueSView** is the *View* component responsible for building the static
  and dynamic HTML structure (head, header, body, footer, scripts) using
  WhakerPy's HTMLTree utilities.

- **TextCueSModel** is an interface with the CuedSpeech automatic annotation.

This structure ensures a clean separation between transport (HTTP),
application logic (Controller), data (Model), and presentation (View), improving
maintainability and scalability of this web interface.

