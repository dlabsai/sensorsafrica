import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { ProcessModule } from "./modules/process/process.module";
import {UserModule} from "./modules/user/user.module";

@Module({
  imports: [
    ConfigModule.forRoot(),
    ProcessModule,
    UserModule,
  ],
})
export class AppModule {}
