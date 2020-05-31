import json, authcli, logging
import fire  # You need this: pip install fire

class TodoList(authcli.Auth):
    """A To-Do list CLI tool managing tasks locally."""
    _client_id = open("client_id.txt").read().strip()  # You ship it with this CLI

    def _data_filename(self):
        return "todo_%s.json" % self._user_id()

    def _load(self):
        return authcli.load_json(self._data_filename(), [])

    def _save(self, data):
        with open(self._data_filename(), 'w') as f:
            json.dump(data, f)

    def list(self):
        return ["{}: {}".format(i, task) for i, task in enumerate(self._load())]

    def add(self, task):
        """Add an task (surrounded by quotation marks) to the end of to-do list.

        Example:

            todo add "Finish my hackathon project"
        """
        self._save(self._load() + [task])

    def done(self, i=0):
        """Delete the i-th task from your to-do list. Default to the first one."""
        data = self._load()
        data.pop(i)
        self._save(data)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Enable log for entire script
    fire.Fire(TodoList)

