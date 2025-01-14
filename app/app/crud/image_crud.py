# app/crud/image.py
from typing import List, Optional
from sqlmodel import Session, select
from ..scema.schema import Image
from typing import List, Optional


class ImageCRUD:
    def create_image(self, session: Session, image: Image) -> Image:
        session.add(image)
        session.commit()
        session.refresh(image)
        return image

    def get_images_by_product(self, session: Session, product_id: int) -> List[Image]:
        statement = select(Image).where(Image.product_id == product_id)
        results = session.execute(statement).scalars().all()
        return results  # type: ignore
    
    def get_image(self, session: Session, image_id: int) -> Optional[Image]:
        return session.get(Image, image_id)

    def delete_image(self, session: Session, image_id: int) -> None:
        image = self.get_image(session, image_id)
        if image:
            session.delete(image)
            session.commit()

image_crud = ImageCRUD()
