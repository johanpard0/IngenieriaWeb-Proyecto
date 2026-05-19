class DocumentIndexObserver:

    def update(self, event_name: str, data: dict):

        if event_name == "file_uploaded":

            print(
                f"Documento pendiente para indexación IA: {data['filename']}"
            )