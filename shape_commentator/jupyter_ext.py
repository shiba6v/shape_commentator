from IPython.core.magic import register_cell_magic
from .main import make_comment, clear_comment, SHAPE_COMMENTATOR_ENV
from IPython.display import Javascript, display
import json

class Ext():
    def __init__(self, global_dict):
        self.env = SHAPE_COMMENTATOR_ENV()
        self.env.globals = global_dict

        @register_cell_magic
        def shape_comment(line, cell):
            output = []
            output_func = lambda x: output.append(x)
            display(Javascript(
                """
                var cell = Jupyter.notebook.get_selected_cell();
                var text = cell.get_text();
                cell.set_text(text.slice(16));
                """
            ))
            make_comment(cell, self.env, output_func)
            output = "\n".join(output)
            new_code = json.dumps({"code": output})
            display(Javascript(
                f"var new_code_json = {new_code}"+"""
                var new_code = new_code_json["code"];
                var cell = Jupyter.notebook.get_selected_cell();
                cell.set_text(new_code);
                """
            ))

        @register_cell_magic
        def shape_erase(line, cell):
            output = []
            output_func = lambda x: output.append(x)
            clear_comment(cell, output_func)
            output = "\n".join(output)
            new_code = json.dumps({"code": output})
            display(Javascript(
                f"var new_code_json = {new_code}"+"""
                var new_code = new_code_json["code"];
                var cell = Jupyter.notebook.get_selected_cell();
                cell.set_text(new_code);
                """
            ))

        def create_button():
            display(Javascript(
            """
            var Jupyter = require('base/js/namespace');
            function shape_comment(){
                var parent = document.getElementsByClassName("end_space")[0];
                while (parent.firstChild) {
                    parent.removeChild(parent.firstChild);
                }
                var cell = Jupyter.notebook.get_selected_cell();
                var orig_text = cell.get_text();
                cell.set_text("%%shape_comment"+"\\n"+orig_text);
                cell.execute();
            }
            if (document.getElementById('shape_commentator_button')!=null){
                document.getElementById('shape_commentator_button').remove();
            }
            if (document.getElementById('shape_commentator_button')==null) {
                Jupyter.toolbar.add_buttons_group([{
                    'label': 'Shape',
                    'icon': 'fa-comment',
                    'callback': shape_comment,
                    'id': 'shape_commentator_button'
                }]);
            }
            
            
            function shape_erase(){
                var parent = document.getElementsByClassName("end_space")[0];
                while (parent.firstChild) {
                    parent.removeChild(parent.firstChild);
                }
                var cell = Jupyter.notebook.get_selected_cell();
                var orig_text = cell.get_text();
                cell.set_text("%%shape_erase"+"\\n"+orig_text);
                cell.execute();
            }
            if (document.getElementById('shape_commentator_erase_button')!=null){
                document.getElementById('shape_commentator_erase_button').remove();
            }
            if (document.getElementById('shape_commentator_erase_button')==null) {
                Jupyter.toolbar.add_buttons_group([{
                    'label': 'Shape',
                    'icon': 'fa-eraser',
                    'callback': shape_erase,
                    'id': 'shape_commentator_erase_button'
                }]);
            }
            """))

        create_button()
