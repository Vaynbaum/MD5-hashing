from common.const import PATH_DIR
from common.work_file import create_not_exist_dir
import recipient
import sender

create_not_exist_dir(PATH_DIR)
sender.root.mainloop()
recipient.root.mainloop()
